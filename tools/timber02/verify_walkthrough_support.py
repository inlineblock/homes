"""Measure modeled support and low crossings along the Timber camera route.

Run with Blender --factory-startup --background --python-exit-code 1 --python
tools/timber02/verify_walkthrough_support.py -- [--model FILE] [--route FILE]
[--output FILE]. Defaults use the published Timber walkthrough and route;
the receipt goes to its ignored outputs/work/walkthrough directory.

This is a read-only, CPU geometry review: it neither saves the scene nor renders.
Support classification is deliberately specific to this Timber model's named
floor, ground, courtyard paving and stepping-slab objects. Finite sampled support
does not establish engineering capacity, safe footfalls or accessible travel.
"""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


ROOT = Path(__file__).resolve().parents[2]
HOME = ROOT / "homes/timber-courtyard-02"
BODY_RADIUS_M = 0.350
CONNECTING_STEP_M = 0.020
HEIGHT_REPORT_THRESHOLD_M = 0.0127
SUPPORT_PREFIXES = (
    "Enclosed floor",
    "Landscape ground",
    "Courtyard paving",
    "Large limestone stepping slab",
)


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model", type=Path, default=HOME / "model/timber-walkthrough.blend"
    )
    parser.add_argument(
        "--route", type=Path, default=HOME / "outputs/videos/camera-route.json"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=HOME / "outputs/work/walkthrough/support-verification.json",
    )
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    args = parser.parse_args(argv)
    for name in ("model", "route", "output"):
        setattr(args, name, getattr(args, name).expanduser().resolve())
    return args


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bounds(points):
    return (
        [min(point[axis] for point in points) for axis in range(3)],
        [max(point[axis] for point in points) for axis in range(3)],
    )


def actual_camera_positions(scene, record):
    """Evaluate every recorded frame; do not infer positions from source code."""
    camera = scene.camera
    if camera is None:
        raise ValueError("The selected scene has no active walkthrough camera")
    poses = record["poses"]
    if len(poses) != record["frame_count"]:
        raise ValueError("Route frame_count disagrees with its pose records")
    positions = []
    maximum_error = 0.0
    for pose in poses:
        scene.frame_set(pose["frame"])
        point = camera.matrix_world.translation.copy()
        error = (point - Vector(pose["position_m"])).length
        maximum_error = max(maximum_error, error)
        positions.append((pose["frame"], point))
    if maximum_error > 0.00001:
        raise ValueError(f"Native camera differs from route by {maximum_error} m")
    scene.frame_set(poses[0]["frame"])
    return positions, maximum_error


def append_mesh(vertices, polygons, names, mesh, points, name):
    offset = len(vertices)
    vertices.extend(points)
    polygons.extend(
        tuple(index + offset for index in face.vertices) for face in mesh.polygons
    )
    names.extend([name] * len(mesh.polygons))


def support_trees(scene, positions):
    """Build evaluated support surfaces and a separate low fixed-mesh surface.

    Landscape plants are not classified as walking support. The separate tree
    retains low architectural rails and the living rug, which the older body
    collision sweep excluded below 50 mm. No library assets are mutated.
    """
    minimum_x = min(point.x for _, point in positions) - BODY_RADIUS_M
    maximum_x = max(point.x for _, point in positions) + BODY_RADIUS_M
    minimum_y = min(point.y for _, point in positions) - BODY_RADIUS_M
    maximum_y = max(point.y for _, point in positions) + BODY_RADIUS_M
    depsgraph = bpy.context.evaluated_depsgraph_get()
    support_vertices, support_faces, support_names = [], [], []
    low_vertices, low_faces, low_names = [], [], []
    inventory, excluded_landscape = [], []

    for obj in scene.objects:
        if obj.library is not None or obj.hide_render or obj.type != "MESH":
            continue
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        try:
            points = [obj.matrix_world @ vertex.co for vertex in mesh.vertices]
            if not points:
                continue
            low, high = bounds(points)
            near_route = (
                high[0] >= minimum_x
                and low[0] <= maximum_x
                and high[1] >= minimum_y
                and low[1] <= maximum_y
                and high[2] >= -0.5
                and low[2] <= 0.20
            )
            if not near_route:
                continue
            landscape = any(
                collection.name.startswith("06 Landscape")
                for collection in obj.users_collection
            )
            is_support = obj.name.startswith(SUPPORT_PREFIXES)
            if is_support:
                append_mesh(
                    support_vertices, support_faces, support_names,
                    mesh, points, obj.name,
                )
                inventory.append({
                    "name": obj.name,
                    "bounds_m": [low, high],
                    "materials": [m.name for m in obj.data.materials if m],
                })
            if not landscape or is_support:
                append_mesh(
                    low_vertices, low_faces, low_names, mesh, points, obj.name
                )
            else:
                excluded_landscape.append(obj.name)
        finally:
            evaluated.to_mesh_clear()

    required = ("Enclosed floor", "Landscape ground", "Courtyard paving")
    if not all(any(item["name"].startswith(prefix) for item in inventory)
               for prefix in required):
        raise ValueError("Expected Timber support objects are missing near the route")
    return {
        "support_tree": BVHTree.FromPolygons(
            support_vertices, support_faces, all_triangles=False
        ),
        "support_names": support_names,
        "low_tree": BVHTree.FromPolygons(low_vertices, low_faces, all_triangles=False),
        "low_names": low_names,
        "inventory": inventory,
        "excluded_landscape": excluded_landscape,
    }


def connecting_samples(positions):
    """Keep every actual pose and add a finite grid between successive poses."""
    samples = [positions[0]]
    for (first_frame, first), (last_frame, last) in zip(positions, positions[1:]):
        divisions = max(1, math.ceil((last - first).length / CONNECTING_STEP_M))
        for index in range(1, divisions + 1):
            fraction = index / divisions
            frame = first_frame + (last_frame - first_frame) * fraction
            samples.append((frame, first.lerp(last, fraction)))
    return samples


def footprint_offsets():
    return [(0.0, 0.0)] + [
        (radius * math.cos(index * math.tau / 16),
         radius * math.sin(index * math.tau / 16))
        for radius in (0.175, BODY_RADIUS_M)
        for index in range(16)
    ]


def downward_hit(tree, names, x, y):
    point, normal, index, _ = tree.ray_cast(
        Vector((x, y, 0.25)), Vector((0, 0, -1)), 1.0
    )
    if point is None:
        return None
    return {"surface": names[index], "z_m": point.z, "normal_z": normal.z}


def measure_samples(trees, samples):
    offsets = footprint_offsets()
    centers, missing, mixed, low_crossings = [], [], [], []
    hit_counts = {}
    normal_minimum = 1.0
    for frame, point in samples:
        footprint_hits = []
        for index, (dx, dy) in enumerate(offsets):
            hit = downward_hit(
                trees["support_tree"], trees["support_names"], point.x + dx, point.y + dy
            )
            if hit is None:
                missing.append({
                    "frame": frame, "offset_m": [dx, dy], "xy_m": list(point.xy)
                })
                continue
            footprint_hits.append(hit)
            normal_minimum = min(normal_minimum, hit["normal_z"])
            hit_counts[hit["surface"]] = hit_counts.get(hit["surface"], 0) + 1
            if index == 0:
                feature = downward_hit(
                    trees["low_tree"], trees["low_names"], point.x, point.y
                )
                centers.append({
                    "frame": frame, "xy_m": list(point.xy), "support": hit,
                    "highest_low_fixed_surface": feature,
                    "camera_above_support_m": point.z - hit["z_m"],
                    "camera_above_low_surface_m": (
                        point.z - feature["z_m"] if feature else None
                    ),
                })
                if (feature and feature["surface"] != hit["surface"]
                        and feature["z_m"] - hit["z_m"] > 0.005):
                    low_crossings.append({
                        "frame": frame, "xy_m": list(point.xy),
                        "object": feature["surface"], "top_z_m": feature["z_m"],
                        "rise_over_support_m": feature["z_m"] - hit["z_m"],
                    })
        if footprint_hits:
            heights = [hit["z_m"] for hit in footprint_hits]
            spread = max(heights) - min(heights)
            if spread > HEIGHT_REPORT_THRESHOLD_M:
                mixed.append({
                    "frame": frame, "cross_footprint_height_range_m": spread,
                    "surfaces": sorted({hit["surface"] for hit in footprint_hits}),
                })
    return {
        "centers": centers, "missing": missing, "mixed": mixed,
        "crossings": low_crossings, "hit_counts": hit_counts,
        "minimum_support_normal_z": normal_minimum,
        "footprint_samples_per_position": len(offsets),
    }


def support_intervals(centers):
    intervals = []
    for hit in centers:
        surface = hit["support"]["surface"]
        height = hit["support"]["z_m"]
        if not intervals or intervals[-1]["surface"] != surface:
            intervals.append({
                "surface": surface, "first_frame": hit["frame"],
                "last_frame": hit["frame"], "start_xy_m": hit["xy_m"],
                "end_xy_m": hit["xy_m"], "min_z_m": height, "max_z_m": height,
            })
        else:
            interval = intervals[-1]
            interval["last_frame"] = hit["frame"]
            interval["end_xy_m"] = hit["xy_m"]
            interval["min_z_m"] = min(interval["min_z_m"], height)
            interval["max_z_m"] = max(interval["max_z_m"], height)
    return intervals


def grouped_crossings(crossings):
    groups = []
    for hit in crossings:
        if not groups or groups[-1]["object"] != hit["object"]:
            groups.append({
                "object": hit["object"], "first_frame": hit["frame"],
                "last_frame": hit["frame"], "y_m": hit["xy_m"][1],
                "max_top_z_m": hit["top_z_m"],
                "max_rise_over_support_m": hit["rise_over_support_m"],
            })
        else:
            group = groups[-1]
            group["last_frame"] = hit["frame"]
            group["max_top_z_m"] = max(group["max_top_z_m"], hit["top_z_m"])
            group["max_rise_over_support_m"] = max(
                group["max_rise_over_support_m"], hit["rise_over_support_m"]
            )
    return groups


def geometric_gaps(inventory):
    """Measure this home's named surface boundaries, not abstract code minima."""
    front = sorted(
        [item for item in inventory
         if item["name"].startswith("Large limestone stepping slab")
         and item["bounds_m"][1][1] < 0],
        key=lambda item: item["bounds_m"][0][1],
    )
    floors = [item for item in inventory if item["name"].startswith("Enclosed floor")]
    paving = next(item for item in inventory if item["name"] == "Courtyard paving")
    before_paving = [item for item in floors
                     if item["bounds_m"][1][1] <= paving["bounds_m"][0][1]]
    after_paving = [item for item in floors
                    if item["bounds_m"][0][1] >= paving["bounds_m"][1][1]]
    return {
        "front_stepping_slab_gaps_y": [
            second["bounds_m"][0][1] - first["bounds_m"][1][1]
            for first, second in zip(front, front[1:])
        ],
        "last_front_slab_to_enclosed_floor_y": (
            min(item["bounds_m"][0][1] for item in floors) - front[-1]["bounds_m"][1][1]
            if front else None
        ),
        "courtyard_paving_front_to_floor_y": (
            paving["bounds_m"][0][1]
            - max(item["bounds_m"][1][1] for item in before_paving)
            if before_paving else None
        ),
        "courtyard_paving_rear_to_floor_y": (
            min(item["bounds_m"][0][1] for item in after_paving)
            - paving["bounds_m"][1][1]
            if after_paving else None
        ),
        "basis": (
            "Evaluated surface object bounds. Lower landscape mesh can support "
            "a gap; a hardscape gap does not by itself mean an unsupported void."
        ),
    }


def main():
    args = arguments()
    record = json.loads(args.route.read_text())
    before = sha256(args.model)
    bpy.ops.wm.open_mainfile(filepath=str(args.model), use_scripts=False)
    positions, pose_error = actual_camera_positions(bpy.context.scene, record)
    trees = support_trees(bpy.context.scene, positions)
    samples = connecting_samples(positions)
    measured = measure_samples(trees, samples)
    centers = measured["centers"]
    changes = [
        {
            "from_frame": first["frame"], "to_frame": second["frame"],
            "height_change_m": second["support"]["z_m"] - first["support"]["z_m"],
            "from_surface": first["support"]["surface"],
            "to_surface": second["support"]["surface"],
        }
        for first, second in zip(centers, centers[1:])
        if abs(second["support"]["z_m"] - first["support"]["z_m"])
        > HEIGHT_REPORT_THRESHOLD_M
    ]
    camera_support_heights = [hit["camera_above_support_m"] for hit in centers]
    camera_low_heights = [hit["camera_above_low_surface_m"] for hit in centers
                          if hit["camera_above_low_surface_m"] is not None]
    has_discontinuities = bool(changes or measured["mixed"] or measured["crossings"])
    result = {
        "native_file": str(args.model), "native_sha256": before,
        "route_file": str(args.route), "route_file_sha256": sha256(args.route),
        "model_unchanged": before == sha256(args.model),
        "software": bpy.app.version_string,
        "frame_pose_count": len(positions),
        "total_sampled_positions": len(samples),
        "intermediate_sample_count": len(samples) - len(positions),
        "maximum_connecting_sample_spacing_m": CONNECTING_STEP_M,
        "max_camera_pose_error_m": pose_error,
        "body_footprint_diameter_m": BODY_RADIUS_M * 2,
        "footprint_samples_per_position": measured["footprint_samples_per_position"],
        "support_ray_count": len(samples) * measured["footprint_samples_per_position"],
        "support_meshes": trees["inventory"],
        "support_hit_counts": measured["hit_counts"],
        "missing_support_ray_count": len(measured["missing"]),
        "missing_support_examples": measured["missing"][:20],
        "center_support_intervals": support_intervals(centers),
        "center_surface_changes_over_12_7mm": changes,
        "max_sampled_center_height_change_m": max(
            (abs(change["height_change_m"]) for change in changes), default=0
        ),
        "mixed_height_footprint_count": len(measured["mixed"]),
        "max_cross_footprint_height_range_m": max(
            (hit["cross_footprint_height_range_m"] for hit in measured["mixed"]),
            default=0,
        ),
        "mixed_height_examples": measured["mixed"][:12],
        "low_fixed_crossings": grouped_crossings(measured["crossings"]),
        "minimum_support_normal_z": measured["minimum_support_normal_z"],
        "excluded_nearby_landscape_objects": len(trees["excluded_landscape"]),
        "landscape_ground_ray_count": measured["hit_counts"].get("Landscape ground", 0),
        "camera_height_above_support_range_m": (
            [min(camera_support_heights), max(camera_support_heights)]
            if camera_support_heights else None
        ),
        "camera_height_above_highest_low_fixed_mesh_range_m": (
            [min(camera_low_heights), max(camera_low_heights)] if camera_low_heights else None
        ),
        "measured_geometric_gaps_m": geometric_gaps(trees["inventory"]),
        "scope_conclusion": (
            "Modeled support exists at every tested point"
            if not measured["missing"] else "Some tested route points lack modeled support"
        ),
        "walking_surface_conclusion": (
            "Measured surface discontinuities or raised low crossings are present; "
            "this is not evidence of a continuous level or step-free route."
            if has_discontinuities else
            "No discontinuity was found at the tested points; finite sampling "
            "does not establish a fully level or accessible route."
        ),
        "method": (
            "Fresh CPU Blender reopen; actual camera locations at all recorded frames. "
            "Linear connecting samples at no more than 20 mm spacing. The center plus "
            "16 points on each of the 175 mm and 350 mm rings sample a 700 mm "
            "circular body footprint. Downward rays run from Z = 250 mm to −750 mm "
            "through evaluated named support "
            "meshes. A separate fixed low-mesh tree retains threshold rails and rug."
        ),
        "limitations": [
            "Finite rays do not verify the unsampled surface between them. Connecting "
            "samples use linear segments between frame poses, not every animation subframe.",
            "Support classification is specific to Timber's named local floor/ground/"
            "paving/slab meshes. Linked furniture and vegetation are not walking support.",
            "Landscape ground is a soil/mulch visualization mesh, not verified pavement, "
            "engineered substrate, bearing capacity, survey grade or slip resistance.",
            "No footfall gait or locomotion animation is tested. Camera height over "
            "measured surfaces is reported separately from its nominal world height.",
            "Low rails are measured fixed geometry, not a manufacturer-tested threshold. "
            "This review does not approve real walking safety, code or accessibility.",
            "No scene save, rendering or GPU use. This receipt alone does not promote "
            "a video or change the home's review status.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    summary_keys = (
        "native_sha256", "frame_pose_count", "total_sampled_positions",
        "intermediate_sample_count", "support_ray_count", "missing_support_ray_count",
        "max_sampled_center_height_change_m", "low_fixed_crossings", "scope_conclusion",
    )
    print(json.dumps({key: result[key] for key in summary_keys}, indent=2), flush=True)
    print("SUPPORT_REVIEW_SAVED", str(args.output), flush=True)


if __name__ == "__main__":
    main()
