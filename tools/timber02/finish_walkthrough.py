"""Run a geometry-conditioned AI finishing candidate, never promote automatically.

Requires a separately installed ltx-2-mlx runtime and compatible local weights.
Models, runtime environments and generated frame caches must stay outside Git.
"""
import argparse
import json
from pathlib import Path
import subprocess
import shutil
from hashlib import sha256

CONTROL_FILTER = ('scale=768:448:force_original_aspect_ratio=increase,crop=768:448,'
                  'edgedetect=low=0.08:high=0.2,format=yuv420p')

ROOT = Path(__file__).resolve().parents[2]
HOME = ROOT / 'homes/timber-courtyard-02'
WORK = HOME / 'outputs/work/walkthrough'
PROMPT = (
    'A continuous photoreal architectural walking tour of this exact timber courtyard home. '
    'The camera smoothly walks forward at eye level along the pale stone entry path toward '
    'the open glazed entrance. Match the camera trajectory, parallax, roof lines, window '
    'mullions, cedar posts and all geometry in the control video. Preserve the exact house '
    'and warm honey cedar, dark standing seam roof, pale limestone paving and red Japanese '
    'maple shown in the photographic reference. Natural fine wood grain, physically realistic '
    'glass reflections, soft warm afternoon daylight and botanically realistic foliage. '
    'Quiet stabilized architectural cinematography, fixed focal length, no cuts, no zoom, '
    'no people, no text, no music or narration. Do not redesign or morph the building.'
)

def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()

def input_fingerprint(start, count, prompt, images, args):
    """Bind a candidate to actual pixels, references, source and generation settings."""
    route = json.loads((WORK / 'route.json').read_text())
    assert digest(HOME / route['source']) == route['source_sha256'], 'Canonical source changed; rebuild native frames.'
    runtime = json.loads((HOME / 'outputs/videos/ai-runtime.json').read_text())
    frames = [digest(WORK / 'frames' / f'frame-{f:04}.png') for f in range(start, start + count)]
    inputs = {'schema': 1, 'source_sha256': route['source_sha256'],
              'route_sha256': digest(WORK / 'route.json'), 'frames_sha256': frames,
              'prompt': prompt, 'images': [{'frame': frame, 'sha256': digest(path)} for path, frame in images],
              'settings': {'width': 768, 'height': 448, 'fps': 24, 'seed': 42,
                           'single_stage': True, 'low_ram': True, 'conditioning': 1.0,
                           'control_filter': CONTROL_FILTER},
              'runtime': runtime['runtime'], 'weights': runtime['weights'],
              'runtime_executable_sha256': digest(args.runtime)}
    return sha256(json.dumps(inputs, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def matching_receipt(path, fingerprint, video):
    if not path.exists() or not video.exists():
        return False
    record = json.loads(path.read_text())
    return (record.get('input_fingerprint') == fingerprint
            and record.get('output_sha256') == digest(video))

def validate_references():
    record = json.loads((HOME / 'outputs/videos/reference-provenance.json').read_text())
    route = json.loads((WORK / 'route.json').read_text())
    poses = {pose['frame']: pose for pose in route['poses']}
    for view in record['views']:
        assert digest(HOME / 'outputs/videos' / view['source']) == view['source_sha256'], view['view']
        assert digest(HOME / 'outputs/videos' / view['image']) == view['image_sha256'], view['view']
        source_frame = view.get('source_frame', view['frame'])
        actual = WORK / 'frames' / f"frame-{source_frame:04}.png"
        assert digest(actual) == view['source_sha256'], f"Stale native reference: {view['view']}"
        if source_frame != view['frame']:
            # Same held camera, with render metadata/noise permitted to differ.
            for field in ['position_m', 'target_m']:
                assert poses[source_frame][field] == poses[view['frame']][field], 'Reference reuse requires an identical held camera pose.'
    return record

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', required=True, type=Path, help='ltx-2-mlx executable')
    parser.add_argument('--models', required=True, type=Path, help='Directory with model/, gemma/, control/')
    parser.add_argument('--ffmpeg', default='ffmpeg')
    parser.add_argument('--frames', type=int, default=97)
    parser.add_argument('--continue-tour', action='store_true', help='Continue a visually accepted 97-frame test through the complete route')
    parser.add_argument('--edited-tour', action='store_true', help='Assemble with one disclosed living-to-kitchen cut, omitting the rejected fast-turn segment')
    parser.add_argument('--retimed-turn-span', choices=['test', 'a', 'b', 'c', 'd'], help='Generate a review-only native-controlled turn span slowed three times; test peak motion first')
    parser.add_argument('--turn-control-mode', choices=['raw', 'clean'], default='raw', help='Optional turn-only smoothing before edge detection; other clips remain unchanged')
    parser.add_argument('--segment-limit', type=int, choices=range(1,9), default=8, help='Stop after this many segments for intermediate review')
    args = parser.parse_args()
    if args.retimed_turn_span:
        retimed_turn_span(args)
        return
    if args.continue_tour:
        continue_tour(args)
        return
    assert args.frames > 1 and (args.frames - 1) % 8 == 0
    control = WORK / 'control-test.mp4'
    candidate = WORK / 'ai-test.mp4'
    subprocess.run([
        args.ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-framerate', '24',
        '-start_number', '1', '-i', str(WORK / 'frames/frame-%04d.png'),
        '-frames:v', str(args.frames), '-vf',
        CONTROL_FILTER,
        '-c:v', 'libx264', '-crf', '16', str(control)
    ], check=True)
    command = [
        str(args.runtime), 'ic-lora', '--model', str(args.models / 'model'),
        '--gemma', str(args.models / 'gemma'), '--lora',
        str(args.models / 'control/ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors'), '1.0',
        '--video-conditioning', str(control), '1.0', '--image',
        str(HOME / 'outputs/videos/references/arrival-photo.png'), '0', '1.0',
        '--prompt', PROMPT, '--frame-rate', '24', '--frames', str(args.frames),
        '--width', '768', '--height', '448', '--single-stage', '--low-ram',
        '--seed', '42', '--output', str(candidate)
    ]
    validate_references()
    fingerprint = input_fingerprint(1, args.frames, PROMPT, [(HOME / 'outputs/videos/references/arrival-photo.png', 0)], args)
    receipt = {'input_fingerprint': fingerprint, 'prompt': PROMPT, 'command': command,
               'status': 'candidate_requested_not_reviewed',
               'aspect_note': 'Control and reference are center-cropped to the model grid.'}
    (WORK / 'ai-test-request.json').write_text(json.dumps(receipt, indent=2) + '\n')
    subprocess.run(command, check=True)
    receipt['output_sha256'] = digest(candidate)
    receipt['status'] = 'rendered_requires_visual_review'
    (WORK / 'ai-test-request.json').write_text(json.dumps(receipt, indent=2) + '\n')


def retimed_turn_span(args):
    """Test the peak yaw, then replace only the fast turn using real native frames.

    Repeat ordered control frames three times; the video model synthesizes the
    slower motion. No photographic slide interpolation, zoom or source redesign.
    This writes ignored candidates only. Review the test before the full spans.
    """
    reference_record = validate_references()
    folder = WORK / ('ai-turn-retimed-clean' if args.turn_control_mode == 'clean' else 'ai-turn-retimed')
    folder.mkdir(exist_ok=True)
    control_filter = (('scale=768:448:force_original_aspect_ratio=increase,crop=768:448,'
                       'gblur=sigma=3,edgedetect=low=0.1:high=0.2,format=yuv420p')
                      if args.turn_control_mode == 'clean' else CONTROL_FILTER)
    records = json.loads((WORK / 'ai-segments/segments.json').read_text())
    original = next(record for record in records if record['segment'] == 5)
    if 'prompt' not in original:
        # Edited reproduction omits the rejected turn. Its optional diagnostic
        # still needs the historical attempted request, never an invented recipe.
        request_path = WORK / 'ai-segments/segment-05-request.json'
        assert request_path.is_file(), 'Retimed diagnostics require a prior rejected turn request.'
        request = json.loads(request_path.read_text())
        command = request['command']
        original = {'prompt': command[command.index('--prompt') + 1],
                    'input_fingerprint': request['input_fingerprint']}
    spans = {'test': (505, 521), 'a': (481, 505), 'b': (505, 529),
             'c': (529, 553), 'd': (553, 577)}
    label = args.retimed_turn_span
    start, end = spans[label]
    count = (end - start) * 3 + 1
    frame_map = [start + index // 3 for index in range(count)]
    images = []
    if label == 'test':
        images.append((HOME / 'outputs/videos/references/turn-living-photo.png', 0))
    elif label == 'a':
        images.append((WORK / 'ai-segments/boundary-05.png', 0))
    else:
        previous = folder / f'span-{chr(ord(label)-1)}.mp4'
        assert previous.is_file(), 'Generate and review the preceding span first.'
        shared = folder / f'shared-frame-{start}.png'
        subprocess.run([args.ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
                        '-i', str(previous), '-vf', 'select=eq(n\\,72)',
                        '-frames:v', '1', str(shared)], check=True)
        images.append((shared, 0))
    for view in reference_record['views']:
        if start < view['frame'] <= end:
            path = (WORK / 'ai-segments/boundary-06.png' if view['frame'] == 577
                    else HOME / 'outputs/videos' / view['image'])
            images.append((path, (view['frame'] - start) * 3))
    prompt = original['prompt'] + ' Turn slowly and steadily. Keep every black window mullion perfectly straight and every countertop rigid, with sharp stable material detail.'
    base_fingerprint = input_fingerprint(start, end - start + 1, prompt, images, args)
    fingerprint = sha256(json.dumps({'base_fingerprint': base_fingerprint,
                                    'source_frame_map': frame_map, 'fps': 24,
                                    'actual_control_filter': control_filter},
                                   sort_keys=True).encode()).hexdigest()
    video = folder / f'span-{label}.mp4'
    receipt_path = folder / f'span-{label}-request.json'
    if matching_receipt(receipt_path, fingerprint, video):
        print('RETIMED_TURN_CACHED_REQUIRES_REVIEW', video, flush=True)
        return
    control_frames = folder / f'control-frames-{label}'
    control_frames.mkdir(exist_ok=True)
    for index, native_frame in enumerate(frame_map, 1):
        path = control_frames / f'frame-{index:04}.png'
        path.unlink(missing_ok=True)
        path.symlink_to(WORK / 'frames' / f'frame-{native_frame:04}.png')
    control = folder / f'control-{label}.mp4'
    subprocess.run([args.ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
                    '-framerate', '24', '-i', str(control_frames / 'frame-%04d.png'),
                    '-frames:v', str(count), '-vf', control_filter,
                    '-c:v', 'libx264', '-crf', '16', str(control)], check=True)
    command = [str(args.runtime), 'ic-lora', '--model', str(args.models / 'model'),
               '--gemma', str(args.models / 'gemma'), '--lora',
               str(args.models / 'control/ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors'), '1.0',
               '--video-conditioning', str(control), '1.0']
    for path, frame in images:
        command += ['--image', str(path), str(frame), '1.0']
    command += ['--prompt', prompt, '--frame-rate', '24', '--frames', str(count),
                '--width', '768', '--height', '448', '--single-stage', '--low-ram',
                '--seed', '42', '--output', str(video)]
    receipt = {'status': 'candidate_requested_not_reviewed', 'source_frames': [start, end],
               'output_frame_count': count, 'source_frame_map': frame_map,
               'retiming': 'Threefold slower true native camera trajectory; repeated ordered control frames, synthesized AI motion.',
               'input_fingerprint': fingerprint, 'base_fingerprint': base_fingerprint,
               'original_segment_input_fingerprint': original['input_fingerprint'],
               'prompt': prompt, 'control_filter': control_filter,
               'images': [{'path': str(path.relative_to(HOME)), 'frame': frame,
                           'sha256': digest(path)} for path, frame in images], 'command': command}
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
    subprocess.run(command, check=True)
    receipt['output_sha256'] = digest(video)
    receipt['status'] = 'rendered_requires_visual_review'
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
    print('RETIMED_TURN_CANDIDATE_REQUIRES_REVIEW', video, flush=True)


def continue_tour(args):
    """Carry the previous boundary frame into each following control-guided segment."""
    parts = WORK / 'ai-segments'
    parts.mkdir(exist_ok=True)
    initial = WORK / 'ai-test.mp4'
    assert initial.is_file(), 'Render and visually approve the 97-frame test first.'
    probe = str(Path(args.ffmpeg).with_name('ffprobe'))
    def complete_clip(path, count):
        if not path.is_file(): return False
        result = subprocess.run([probe, '-v', 'error', '-select_streams', 'v:0',
                                 '-show_entries', 'stream=nb_frames,width,height,r_frame_rate',
                                 '-of', 'json', str(path)], capture_output=True, text=True)
        if result.returncode: return False
        streams = json.loads(result.stdout).get('streams', [])
        return bool(streams and streams[0].get('nb_frames') == str(count)
                    and streams[0].get('width') == 768 and streams[0].get('height') == 448
                    and streams[0].get('r_frame_rate') == '24/1')
    assert complete_clip(initial, 97), 'Initial test is incomplete or uses different settings.'
    assert all((WORK/'frames'/f'frame-{f:04}.png').exists() for f in range(1,722))
    reference_record = validate_references()
    initial_fingerprint = input_fingerprint(1, 97, PROMPT, [(HOME / 'outputs/videos/references/arrival-photo.png', 0)], args)
    assert matching_receipt(WORK / 'ai-test-request.json', initial_fingerprint, initial), 'Initial test inputs changed; regenerate and review it.'
    references = sorted((view['frame']-1, view['view']) for view in reference_record['views'])
    boundary_record = HOME/'outputs/videos/boundary-anchors.json'
    fixed_boundaries = {}
    if boundary_record.exists():
        boundary_data = json.loads(boundary_record.read_text())
        assert boundary_data.get('source_sha256') == json.loads((WORK / 'route.json').read_text())['source_sha256'], 'Stale fixed boundaries; retire them before refreshing the tour.'
        for item in boundary_data['anchors']:
            path = HOME/'outputs/videos'/item['image']
            assert sha256(path.read_bytes()).hexdigest() == item['sha256']
            fixed_boundaries[item['frame']-1] = path
    if args.edited_tour:
        assert 576 in fixed_boundaries, 'Edited reproduction requires the reviewed AI-derived native-frame577 boundary in boundary-anchors.json.'
    actions = [
        'Walk forward toward the open front entrance.',
        'Walk under the canopy and through the open glazed front entrance.',
        'Walk through the open garden threshold along the stone courtyard path.',
        'Walk toward the open rear glazed gable, passing right of its central cedar post.',
        'Enter the living room through the open glazing and turn left toward the cream sofa.',
        'Pause and turn smoothly right from the living room toward the dining area and kitchen.',
        'Walk along the clear aisle beside the dining table toward the kitchen island.',
        'Slow to a stop beside the kitchen island and look across the kitchen.'
    ]
    base = (
        'A continuous photoreal architectural walking tour of the exact same timber courtyard home. '
        'Follow the camera movement, parallax, framing and geometry of the control video precisely. '
        'Preserve all walls, glazing mullions, cedar posts, roof slopes, openings and furniture positions. '
        'Match the reference images: honey cedar, black glazing frames, cream plaster and upholstery, '
        'pale limestone, pale oak dining furniture, smoked-oak kitchen cabinets and sage green tile. '
        'Where visible, retain the exact stainless hood, induction hob, built-in oven, sink, cabinet '
        'doors and fitted pantry shelves; never remove, replace or relocate them. '
        'The peaked ceiling and upper walls behind the rear gable glazing are solid honey cedar, '
        'never sky or transparent surfaces. Keep their exact boundaries from the reference. '
        'Natural material texture, realistic glass reflections and soft warm afternoon light. Fixed lens, stable eye height, '
        'no cuts, no zoom, no people, no new architecture, no furniture changes, no text or narration. '
    )
    records = []
    previous = None
    for index, start in enumerate(range(0, 720, 96)):
        if index >= args.segment_limit:
            print('AI_PARTIAL_REVIEW_STOP', index, flush=True)
            return
        if (WORK / 'STOP-AI-TOUR').exists():
            raise RuntimeError('Stopped between segments for visual review.')
        if args.edited_tour and index == 5:
            records.append({'segment': 5, 'source_frames': [481, 577],
                            'excluded_from_edited_tour': True,
                            'reason': 'Rejected fast turn; reviewed frame577 boundary starts the kitchen shot.'})
            continue
        count = min(97, 721 - start)
        video = parts / f'segment-{index:02}.mp4'
        if index == 0:
            if not complete_clip(video, count) or digest(video) != digest(initial): shutil.copy2(initial, video)
            records.append({'segment': index, 'source_frames': [1,97], 'reused_test_sha256':sha256(initial.read_bytes()).hexdigest()})
        else:
            boundary = parts / f'boundary-{index:02}.png'
            if start in fixed_boundaries:
                shutil.copy2(fixed_boundaries[start], boundary)
            else:
                subprocess.run([args.ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(previous),
                                '-vf', 'select=eq(n\\,96)', '-frames:v', '1', str(boundary)], check=True)
            control = parts / f'control-{index:02}.mp4'
            subprocess.run([args.ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-framerate', '24',
                            '-start_number', str(start+1), '-i', str(WORK/'frames/frame-%04d.png'),
                            '-frames:v', str(count), '-vf', CONTROL_FILTER,
                            '-c:v', 'libx264', '-crf', '16', str(control)], check=True)
            prompt = base + actions[index]
            command = [str(args.runtime), 'ic-lora', '--model', str(args.models/'model'),
                       '--gemma', str(args.models/'gemma'), '--lora',
                       str(args.models/'control/ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors'), '1.0',
                       '--video-conditioning', str(control), '1.0', '--image', str(boundary), '0', '1.0']
            anchors = []
            fingerprint_images = [(boundary, 0)]
            for frame, name in references:
                if start < frame <= start+count-1:
                    reference = fixed_boundaries.get(frame, HOME/f'outputs/videos/references/{name}-photo.png')
                    command += ['--image', str(reference), str(frame-start), '1.0']
                    fingerprint_images.append((reference, frame-start))
                    anchors.append({'reference': name, 'local_frame_index': frame-start,
                                    'image':str(reference.relative_to(HOME/'outputs/videos')),
                                    'sha256':sha256(reference.read_bytes()).hexdigest()})
            command += ['--prompt', prompt, '--frame-rate', '24', '--frames', str(count),
                        '--width', '768', '--height', '448', '--single-stage', '--low-ram',
                        '--seed', '42', '--output', str(video)]
            records.append({'segment':index, 'source_frames':[start+1,start+count], 'prompt':prompt,
                            'previous_boundary':boundary.name, 'boundary_image_sha256':sha256(boundary.read_bytes()).hexdigest(),
                            'fixed_shared_boundary':str(fixed_boundaries[start].relative_to(HOME/'outputs/videos')) if start in fixed_boundaries else None,
                            'imagegen_anchors':anchors})
            fingerprint = input_fingerprint(start+1, count, prompt, fingerprint_images, args)
            cache_receipt = parts / f'segment-{index:02}-request.json'
            if not complete_clip(video, count) or not matching_receipt(cache_receipt, fingerprint, video):
                subprocess.run(command, check=True)
                cache_receipt.write_text(json.dumps({'input_fingerprint': fingerprint, 'command': command,
                                                     'output_sha256': digest(video)}, indent=2) + '\n')
            records[-1]['input_fingerprint'] = fingerprint
        assert complete_clip(video, count), f'Incomplete clip: {video}'
        records[-1]['output_sha256'] = sha256(video.read_bytes()).hexdigest()
        previous = video
        (parts/'segments.json').write_text(json.dumps(records,indent=2)+'\n')
        print('AI_SEGMENT_READY', index, str(video), flush=True)
    # Remove overlapping boundary frames, retain camera travel and omit AI audio.
    # A purposeful editorial cut can omit a visually rejected turn; it is recorded
    # explicitly and never described as a continuous uncut AI take.
    selected = [0, 1, 2, 3, 4, 6, 7] if args.edited_tour else list(range(8))
    sequence = parts/('edited-frames' if args.edited_tour else 'assembled-frames')
    sequence.mkdir(exist_ok=True)
    next_frame = 1
    source_frame_map = []
    shots = []
    previous_index = None
    for index in selected:
        start = index * 96
        drop_overlap = previous_index is not None and index == previous_index + 1
        count = min(97,721-start) - int(drop_overlap)
        command = [args.ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i',str(parts/f'segment-{index:02}.mp4')]
        if drop_overlap:command += ['-vf', 'select=gt(n\\,0)']
        command += ['-fps_mode','vfr','-start_number',str(next_frame),str(sequence/'frame-%04d.png')]
        subprocess.run(command,check=True)
        first_source = start + 1 + int(drop_overlap)
        source_frame_map.extend(range(first_source, first_source + count))
        shots.append({'segment': index, 'output_frames': [next_frame, next_frame + count - 1],
                      'source_frames': [first_source, first_source + count - 1],
                      'transition': 'start' if previous_index is None else ('continuous' if drop_overlap else 'editorial_cut')})
        next_frame += count
        previous_index = index
    frame_count = next_frame - 1
    assert frame_count == (626 if args.edited_tour else 721)
    candidate = WORK/('timber-courtyard-ai-edited-candidate.mp4' if args.edited_tour else 'timber-courtyard-ai-candidate.mp4')
    subprocess.run([args.ffmpeg,'-hide_banner','-loglevel','error','-y','-framerate','24',
                    '-i',str(sequence/'frame-%04d.png'),'-frames:v',str(frame_count),'-c:v','libx264',
                    '-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(candidate)],check=True)
    assembly = {'status': 'candidate_requires_visual_review', 'fps': 24, 'frame_count': frame_count,
                'duration_seconds': frame_count / 24, 'silent': True, 'shots': shots,
                'source_frame_map': source_frame_map, 'output_sha256': digest(candidate),
                'excluded_source_frames': [482, 576] if args.edited_tour else None,
                'editorial_note': 'One clean cut from the living pause to kitchen approach replaces a rejected AI turn. All retained shots use native camera movement; no slideshow, zoom or synthetic photo pan.' if args.edited_tour else 'Continuous route candidate; review every join before promotion.'}
    (WORK / ('edited-assembly.json' if args.edited_tour else 'continuous-assembly.json')).write_text(json.dumps(assembly, indent=2)+'\n')
    print('AI_TOUR_CANDIDATE_REQUIRES_VISUAL_REVIEW',candidate,flush=True)

if __name__ == '__main__':
    main()
