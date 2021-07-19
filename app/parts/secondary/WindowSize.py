import random


class WindowSize:

    def get_size():

        sizes_list = [
            {
                'width': 1280,
                'height': 720
            },
            {
                'width': 1280,
                'height': 768
            },
            {
                'width': 1280,
                'height': 1024
            },
            {
                'width': 1440,
                'height': 900
            },
            {
                'width': 1400,
                'height': 1050
            },
            {
                'width': 1536,
                'height': 960
            },
            {
                'width': 1536,
                'height': 1024
            },
            {
                'width': 1600,
                'height': 900
            },
            {
                'width': 1600,
                'height': 1024
            },
            {
                'width': 1600,
                'height': 1200
            },
            {
                'width': 1680,
                'height': 1050
            },
            {
                'width': 1920,
                'height': 1080
            },
            {
                'width': 1920,
                'height': 1200
            },
            {
                'width': 2048,
                'height': 1080
            },
            {
                'width': 2048,
                'height': 1152
            },
            {
                'width': 2048,
                'height': 1536
            },
            {
                'width': 2560,
                'height': 1440
            },
            {
                'width': 2560,
                'height': 1600
            },
            {
                'width': 2560,
                'height': 2048
            },
            {
                'width': 3200,
                'height': 2048
            },
            {
                'width': 3200,
                'height': 2400
            },
            {
                'width': 3840,
                'height': 2400
            },
            {
                'width': 4096,
                'height': 2160
            },
            {
                'width': 5120,
                'height': 4096
            },
            {
                'width': 6400,
                'height': 4096
            },
            {
                'width': 6400,
                'height': 4800
            },
            {
                'width': 7680,
                'height': 4320
            },
            {
                'width': 7680,
                'height': 4800
            }
        ]
    
        return random.choice(sizes_list)