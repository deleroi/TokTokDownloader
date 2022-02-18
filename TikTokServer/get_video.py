import glob, os, socket, time, zipfile
import cv2
from TikTokApi import TikTokApi


api = TikTokApi()

# Receiving video in format mp4 from TikTok using ID_Video.
def get_video(id_video):
    video = api.video(id=id_video)
    video_data = video.bytes()
    with open("video/out.mp4", "wb") as out_file:
        out_file.write(video_data)

# Getting a series of frames in JPG format from a video.
def convert_mp4_to_jpgs(path):
    video_capture = cv2.VideoCapture(path)
    still_reading, image = video_capture.read()
    frame_count = 0
    while still_reading:
        cv2.imwrite(f"output/{frame_count:03d}.jpg", image)
        # read next image
        still_reading, image = video_capture.read()
        frame_count += 1

# File deletion function
def delete_files():
    files = glob.glob('./output/*.jpg', recursive=True)
    for f in files:
        os.remove(f)
    video_path = './video/out.mp4'
    os.remove(video_path)
    zip_path = './test.zip'
    os.remove(zip_path)
    print("All file deleted")


if __name__ == "__main__":

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 9090))
    serversocket.listen(5)  # become a server socket, maximum 5 connections

    while True:
        conn, addr = serversocket.accept()
        id_video = conn.recv(1024)
        data = bytes.decode(id_video)
        if id_video:
            get_video(data)
            convert_mp4_to_jpgs("video/out.mp4")

            # add to zip
            path = 'output/'
            file_dir = os.listdir(path)
            with zipfile.ZipFile('test.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
                for file in file_dir:
                    add_file = os.path.join(path, file)
                    zf.write(add_file)

            # Sending zip archive to client.
            file_name = "test.zip"
            file_size = os.path.getsize(file_name)

            # Send the file details to the client.
            conn.send(file_name.encode())
            conn.send(str(file_size).encode())

            # Open and read the file.
            with open(file_name, "rb") as file:
                c = 0

                # Start the time capture.
                start_time = time.time()

                # Running the loop while the file  sent.
                while c < file_size:
                    data = file.read(1024)
                    if not (data):
                        break
                    conn.sendall(data)
                    c += len(data)

                # End the time capture.
                end_time = time.time()

            print("File transfer complete. Total time: ", end_time - start_time)

            # Delete files after transfer
            delete_files()
            conn.close()










