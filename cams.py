from Stream import Stream
from multiprocessing import Process


streams = []

if __name__ == '__main__':

    streams.append(Stream("cam0", "https://www.youtube.com/watch?v=gcDWT-mTCOI"))
    streams.append(Stream("cam1", "https://www.youtube.com/watch?v=BQFGmIXwl-A"))

    for cam in streams:
        cam.simulate_url()
        cam_process = Process(target=cam.get_frames)
        cam_process.start()
