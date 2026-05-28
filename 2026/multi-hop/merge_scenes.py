import os
import subprocess

def main():
    scenes = [
        "Scene1SimpleRAGFailure",
        "Scene2ParallelDecomposition",
        "Scene3ParallelDecompositionFailure",
        "Scene4SequentialMultiHop",
        "Scene5Tradeoffs"
    ]
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_txt_path = os.path.join(current_dir, "inputs.txt")
    output_mp4_path = os.path.join(current_dir, "multi_hop_merged.mp4")
    
    print("Preparing inputs.txt for ffmpeg...")
    with open(input_txt_path, "w") as f:
        for scene in scenes:
            scene_file = f"{scene}.mp4"
            scene_path = os.path.join(current_dir, scene_file)
            if not os.path.exists(scene_path):
                print(f"Error: {scene_file} not found in {current_dir}!")
                return
            f.write(f"file '{scene_path}'\n")
            
    print(f"Concatenating files into {output_mp4_path}...")
    command = f"ffmpeg -y -f concat -safe 0 -i \"{input_txt_path}\" -c copy \"{output_mp4_path}\""
    print(f"Running: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("Success! Merged video created at:", output_mp4_path)
    else:
        print("Error during concatenation:")
        print(result.stderr)
        
    if os.path.exists(input_txt_path):
        os.remove(input_txt_path)

if __name__ == "__main__":
    main()
