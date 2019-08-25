import argparse

def make_parser():
    parser = argparse.ArgumentParser(description='Meani.mo Vision')
    parser.add_argument('--drone_path', default='Hello World!', required=False, help='Drone Image')
    
    
    return parser.parse_args()






