import logging
from pathlib import Path

from svl.localization.map_reader import SatelliteMapReader
from svl.localization.drone_streamer import DroneImageStreamer
from svl.localization.preprocessing import QueryProcessor
# from svl.localization.pipeline import Pipeline, PipelineConfig
from svl.localization.pipeline import Pipeline, PipelineConfig

from svl.keypoint_pipeline.typing import SuperGlueConfig, SuperPointConfig
from svl.keypoint_pipeline.detection_and_description import SuperPointAlgorithm
from svl.keypoint_pipeline.matcher import SuperGlueMatcher

from svl.tms.data_structures import CameraModel
if __name__ == "__main__":
    # Setup logginhg for information
    # logging.basicConfig(level=logging.INFO)
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    # Setup the keypoint detector
    superpoint_config = SuperPointConfig(
        device="cuda",
        nms_radius=4,
        keypoint_threshold=0.01,
        max_keypoints=-1,
    )
    superpoint_algorithm = SuperPointAlgorithm(superpoint_config)

    # Setup the keypoint matcher
    superglue_config = SuperGlueConfig(
        device="cuda",
        weights="outdoor",
        sinkhorn_iterations=20,
        match_threshold=0.5,
    )
    superglue_matcher = SuperGlueMatcher(superglue_config)

    # Read Satellite Map
    map_reader = SatelliteMapReader(
        db_path="./dataset/georeference/",
        resize_size=(800,),
        logger=logging.getLogger("%s.SatelliteMapReader" % __name__),  # noqa
    )
    map_reader.initialize_db()
    map_reader.setup_db()
    map_reader.resize_db_images() # ???? Unable to find it
    map_reader.describe_db_images(superpoint_algorithm)



    # Read the drone image streamer #TODO: image inpput
    streamer = DroneImageStreamer(
        image_folder="./dataset/query/",
        has_gt=True,
        logger=logging.getLogger("%s.DroneImageStreamer" % __name__),  # noqa
    )
    print('Length: ',len(streamer))

    print('AAAAAAAAAAAAAAAAAAAAAAA')

    # Initialize the query processor # ??????? I don't think we need those
    camera_model = CameraModel(
        focal_length=4.5 / 1000,  # 4.5mm
        resolution_height=4056,
        resolution_width=3040,
        hfov_deg=82.9,
    )
    query_processor = QueryProcessor(
        processings=["resize"],
        camera_model=camera_model,
        satellite_resolution=None,
        size=(800,),
    )

    # Initialize the pipeline # ??????? I don't think we need those
    logger = logging.getLogger("%s.Pipeline" % __name__)  # Change to Pipeline for logging
    logger.setLevel(logging.DEBUG)
    pipeline = Pipeline(
        map_reader=map_reader,
        drone_streamer=streamer,
        detector=superpoint_algorithm,
        matcher=superglue_matcher,
        query_processor=query_processor,
        config=PipelineConfig(),
        # logger=logging.getLogger("%s.Pipeline" % __name__),  # noqa
        logger=logger,
    )

    output_path = "./dataset/results"
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    preds = pipeline.run(
        output_path=output_path,
    )
    print('Prediction: ')
    for pred in preds:
        print('Is match?: ',pred['is_match'])
        print('Prediction: ',pred['predicted_coordinate'])
        print('center: ', pred['center'])
        print('_++++++++++++++++++++++++++++AAAa++')