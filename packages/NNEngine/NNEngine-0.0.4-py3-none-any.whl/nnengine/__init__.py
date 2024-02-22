import os

os.system("pip install timm==0.6.7")
os.system("pip install torch==2.0.1")
os.system("pip install moviepy")


def Depth(input_path):

    import torch
    import cv2
    import os
    import shutil
    import numpy as np
    import pickle
    from moviepy.editor import VideoFileClip, ImageSequenceClip

    repo = "isl-org/ZoeDepth"
    model = torch.hub.load(repo, "ZoeD_K", pretrained=True)

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    zoe = model.to(DEVICE)

    video = VideoFileClip(input_path)
    total_frames = int(video.duration * video.fps)

    frames = []

    for i, frame in enumerate(video.iter_frames()):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        depth = zoe.infer_pil(frame)

        depth = cv2.normalize(depth, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        frames.append(depth)
        print('\r' + str(i) + '/' + str(total_frames), end='')

    frames = np.array(frames, dtype=np.uint8)

    file = open('./Depth.node' 'wb')
    pickle.dump(frames, file)
    file.close()

def Segmentation(input_path,output_path,classes=['person','car'],enable_long_term_count_usage=True, max_num_objects=100, size=480,
                   DINO_THRESHOLD=0.35, amp=True, chunk_size=1, detection_every=2,
                   max_missed_detection_count=10, sam_variant='original',
                   temporal_setting='semionline', pluralize=True):
    
    
    import os
    HOME = os.getcwd()
    print("HOME:", HOME)

    os.chdir(HOME)

    os.system("git clone https://github.com/hkchengrex/Grounded-Segment-Anything")

    os.environ["CUDA_HOME"] = "/usr/local/cuda"
    os.environ["BUILD_WITH_CUDA"] = "True"
    os.environ["AM_I_DOCKER"] = "False"

    os.chdir(os.path.join(HOME, "Grounded-Segment-Anything"))

    os.system("pip uninstall -y GroundingDINO")

    os.system("pip install -e GroundingDINO")

    os.system("pip install -q -e segment_anything")

    import site
    site.main()

    import os
    HOME = os.getcwd()
    print("HOME:", HOME)

    os.chdir(HOME)
    try:
        import groundingdino
        from groundingdino.util.inference import Model as GroundingDINOModel
    except ImportError:
        import GroundingDINO
        from GroundingDINO.groundingdino.util.inference import Model as GroundingDINOModel


    #Installing DEVA

    os.chdir(HOME)

    os.system("git clone https://github.com/hkchengrex/Tracking-Anything-with-DEVA")

    os.chdir(os.path.join(HOME, "Tracking-Anything-with-DEVA"))

    os.system("pip install -q -e .")

    #Downloading Some PreTrained Models

    os.chdir(os.path.join(HOME, "Tracking-Anything-with-DEVA"))

    os.system(
        "wget -q -P ./saves/ https://github.com/hkchengrex/Tracking-Anything-with-DEVA/releases/download/v1.0/DEVA-propagation.pth")
    os.system(
        "wget -q -P ./saves/ https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth")
    os.system("wget -q -P ./saves/ https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth")
    os.system(
        "wget -q -P ./saves/ https://github.com/hkchengrex/Tracking-Anything-with-DEVA/releases/download/v1.0/GroundingDINO_SwinT_OGC.py")

    #MAIN

    os.chdir(os.path.join(HOME, "Tracking-Anything-with-DEVA"))
    import site
    site.main()
    import os
    from os import path
    from argparse import ArgumentParser
    import torch.nn.functional as F
    import torchvision
    import torch
    import numpy as np
    from typing import Dict, List
    from segment_anything import sam_model_registry, SamPredictor
    from deva.ext.MobileSAM.setup_mobile_sam import setup_model as setup_mobile_sam
    from deva.inference.demo_utils import get_input_frame_for_deva
    from deva.inference.frame_utils import FrameInfo
    from deva.inference.object_info import ObjectInfo
    from deva.model.network import DEVA
    from deva.inference.inference_core import DEVAInferenceCore
    from deva.inference.result_utils import ResultSaver
    from deva.inference.eval_args import add_common_eval_args, get_model_and_config
    from deva.inference.demo_utils import flush_buffer
    from deva.ext.ext_eval_args import add_ext_eval_args, add_text_default_args
    from deva.ext.grounding_dino import get_grounding_dino_model
    from segment_anything import SamPredictor
    from tqdm import tqdm
    import json
    import matplotlib.pyplot as plt
    import imageio
    import pickle

    torch.autograd.set_grad_enabled(False)

    # for id2rgb
    np.random.seed(42)

    # default parameters
    parser = ArgumentParser()
    add_common_eval_args(parser)
    add_ext_eval_args(parser)
    add_text_default_args(parser)

    # load model and config
    args = parser.parse_args([])
    cfg = vars(args)
    cfg['enable_long_term'] = True

    # Load our checkpoint
    deva_model = DEVA(cfg).cuda().eval()
    if args.model is not None:
        model_weights = torch.load(args.model)
        deva_model.load_weights(model_weights)
    else:
        print('No model loaded.')

    gd_model, sam_model = get_grounding_dino_model(cfg, 'cuda')

    masks=[]

    def segment_with_text(config: Dict, gd_model: GroundingDINOModel, sam: SamPredictor,
                        image: np.ndarray, prompts: List[str],
                        min_side: int) -> (torch.Tensor, List[ObjectInfo]):
        """
        config: the global configuration dictionary
        image: the image to segment; should be a numpy array; H*W*3; unnormalized (0~255)
        prompts: list of class names

        Returns: a torch index mask of the same size as image; H*W
                a list of segment info, see object_utils.py for definition
        """

        BOX_THRESHOLD = TEXT_THRESHOLD = config['DINO_THRESHOLD']
        NMS_THRESHOLD = config['DINO_NMS_THRESHOLD']

        sam.set_image(image, image_format='RGB')

        # detect objects
        # GroundingDINO uses BGR
        detections = gd_model.predict_with_classes(image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR),
                                                classes=prompts,
                                                box_threshold=BOX_THRESHOLD,
                                                text_threshold=TEXT_THRESHOLD)

        nms_idx = torchvision.ops.nms(torch.from_numpy(detections.xyxy),
                                    torch.from_numpy(detections.confidence),
                                    NMS_THRESHOLD).numpy().tolist()

        detections.xyxy = detections.xyxy[nms_idx]
        detections.confidence = detections.confidence[nms_idx]
        detections.class_id = detections.class_id[nms_idx]

        result_masks = []
        for box in detections.xyxy:
            masks, scores, _ = sam.predict(box=box, multimask_output=True)
            index = np.argmax(scores)
            result_masks.append(masks[index])

        detections.mask = np.array(result_masks)

        h, w = image.shape[:2]
        if min_side > 0:
            scale = min_side / min(h, w)
            new_h, new_w = int(h * scale), int(w * scale)
        else:
            new_h, new_w = h, w

        output_mask = torch.zeros((new_h, new_w), dtype=torch.int64, device=gd_model.device)
        curr_id = 1
        segments_info = []

        # sort by descending area to preserve the smallest object
        for i in np.flip(np.argsort(detections.area)):
            mask = detections.mask[i]
            confidence = detections.confidence[i]
            class_id = detections.class_id[i]
            mask = torch.from_numpy(mask.astype(np.float32))
            mask = F.interpolate(mask.unsqueeze(0).unsqueeze(0), (new_h, new_w), mode='bilinear')[0, 0]
            mask = (mask > 0.5).float()

            if mask.sum() > 0:
                output_mask[mask > 0] = curr_id
                segments_info.append(ObjectInfo(id=curr_id, category_id=class_id, score=confidence))
                curr_id += 1

        return output_mask, segments_info



    def make_segmentation_with_text(cfg: Dict, image_np: np.ndarray, gd_model: GroundingDINOModel,
                                    sam_model: SamPredictor, prompts: List[str],
                                    min_side: int) -> (torch.Tensor, List[ObjectInfo]):
        mask, segments_info = segment_with_text(cfg, gd_model, sam_model, image_np, prompts, min_side)
        return mask, segments_info


    @torch.inference_mode()
    def process_frame(deva: DEVAInferenceCore,
                                gd_model: GroundingDINOModel,
                                sam_model: SamPredictor,
                                frame_path: str,
                                result_saver: ResultSaver,
                                ti: int,
                                image_np: np.ndarray = None) -> None:
        # image_np, if given, should be in RGB
        if image_np is None:
            image_np = cv2.imread(frame_path)
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        cfg = deva.config
        raw_prompt = cfg['prompt']
        prompts = raw_prompt.split('.')

        h, w = image_np.shape[:2]
        new_min_side = cfg['size']
        need_resize = new_min_side > 0
        image = get_input_frame_for_deva(image_np, new_min_side)

        frame_name = path.basename(frame_path)
        frame_info = FrameInfo(image, None, None, ti, {
            'frame': [frame_name],
            'shape': [h, w],
        })

        if cfg['temporal_setting'] == 'semionline':
            if ti + cfg['num_voting_frames'] > deva.next_voting_frame:
                mask, segments_info = make_segmentation_with_text(cfg, image_np, gd_model, sam_model,
                                                                prompts, new_min_side)
                frame_info.mask = mask
                frame_info.segments_info = segments_info
                frame_info.image_np = image_np  # for visualization only
                # wait for more frames before proceeding
                deva.add_to_temporary_buffer(frame_info)

                if ti == deva.next_voting_frame:
                    # process this clip
                    this_image = deva.frame_buffer[0].image
                    this_frame_name = deva.frame_buffer[0].name
                    this_image_np = deva.frame_buffer[0].image_np

                    _, mask, new_segments_info = deva.vote_in_temporary_buffer(
                        keyframe_selection='first')
                    prob = deva.incorporate_detection(this_image, mask, new_segments_info)
                    deva.next_voting_frame += cfg['detection_every']
                    
                    if need_resize:
                        prob = F.interpolate(prob.unsqueeze(1), (h, w), mode='bilinear', align_corners=False)[:,0]
                    # Probability mask -> index mask
                    mask = torch.argmax(prob, dim=0)
                    
                    masks.append(mask.cpu().numpy())
                    
                    result_saver.save_mask(prob,
                        frame_name,
                        need_resize=need_resize,
                        shape=(h, w),
                        image_np=image_np,
                        prompts=prompts)


                    for frame_info in deva.frame_buffer[1:]:
                        this_image = frame_info.image
                        this_frame_name = frame_info.name
                        this_image_np = frame_info.image_np
                        prob = deva.step(this_image, None, None)
                        
                        
                        if need_resize:
                            prob = F.interpolate(prob.unsqueeze(1), (h, w), mode='bilinear', align_corners=False)[:,0]
                        # Probability mask -> index mask
                        mask = torch.argmax(prob, dim=0)

                        masks.append(mask.cpu().numpy())
                        
                        result_saver.save_mask(prob,
                        frame_name,
                        need_resize=need_resize,
                        shape=(h, w),
                        image_np=image_np,
                        prompts=prompts)

                        
                    deva.clear_buffer()
                    
            else:
                # standard propagation
                prob = deva.step(image, None, None)
                
                if need_resize:
                    prob = F.interpolate(prob.unsqueeze(1), (h, w), mode='bilinear', align_corners=False)[:,0]
                # Probability mask -> index mask
                mask = torch.argmax(prob, dim=0)

                masks.append(mask.cpu().numpy())
                
                result_saver.save_mask(prob,
                        frame_name,
                        need_resize=need_resize,
                        shape=(h, w),
                        image_np=image_np,
                        prompts=prompts)



        elif cfg['temporal_setting'] == 'online':
            if ti % cfg['detection_every'] == 0:
                # incorporate new detections
                mask, segments_info = make_segmentation_with_text(cfg, image_np, gd_model, sam_model,
                                                                prompts, new_min_side)
                frame_info.segments_info = segments_info
                prob = deva.incorporate_detection(image, mask, segments_info)
            else:
                # Run the model on this frame
                prob = deva.step(image, None, None)

            image_np=np.zeros_like(image_np,dtype=np.uint8)
            result_saver.save_mask(prob,
                                frame_name,
                                need_resize=need_resize,
                                shape=(h, w),
                                image_np=image_np,
                                prompts=prompts)


    cfg['enable_long_term_count_usage'] = enable_long_term_count_usage
    cfg['max_num_objects'] = max_num_objects
    cfg['size'] = size
    cfg['DINO_THRESHOLD'] = DINO_THRESHOLD
    cfg['amp'] = amp
    cfg['chunk_size'] = chunk_size
    cfg['detection_every'] = detection_every
    cfg['max_missed_detection_count'] = max_missed_detection_count
    cfg['sam_variant'] = sam_variant
    cfg['temporal_setting'] = temporal_setting # temporal_setting usually works better; but online is faster for this demo
    cfg['pluralize'] = pluralize

    SOURCE_VIDEO_PATH = input_path
    CLASSES = classes
    OUTPUT_VIDEO_PATH = output_path


    os.chdir(os.path.join(HOME, "Tracking-Anything-with-DEVA"))
    import cv2
    cfg['prompt'] = '.'.join(CLASSES)

    deva = DEVAInferenceCore(deva_model, config=cfg)
    deva.next_voting_frame = cfg['num_voting_frames'] - 1
    deva.enabled_long_id()

    # obtain temporary directory
    result_saver = ResultSaver(None, None, dataset='gradio', object_manager=deva.object_manager)
    writer_initizied = False

    cap = cv2.VideoCapture(SOURCE_VIDEO_PATH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    ti = 0
    # only an estimate
    with torch.cuda.amp.autocast(enabled=cfg['amp']):
        with tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))) as pbar:
            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    if not writer_initizied:
                        h, w = frame.shape[:2]
                        writer = cv2.VideoWriter(OUTPUT_VIDEO_PATH, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                        writer_initizied = True
                        result_saver.writer = writer

                    process_frame(deva,
                                        gd_model,
                                        sam_model,
                                        'null.png',
                                        result_saver,
                                        ti,
                                        image_np=frame)
                    


                    ti += 1
                    pbar.update(1)
                else:
                    break
        flush_buffer(deva, result_saver)
    writer.release()
    cap.release()
    deva.clear_buffer()

    file=open('Segmentation.node','wb')
    pickle.dump(masks,file)

    file.close()