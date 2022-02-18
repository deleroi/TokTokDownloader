from flask import Flask, render_template, url_for, request, session, redirect
import os
import socket, time, zipfile, glob


app = Flask(__name__)

# File counting and sorting.
def file_count(directory):
    files = os.listdir(directory)
    files.sort()
    return files

# Unpacking the archive with frames.
def unpack_zip():
    print('Extracting ZIP.')
    archive = zipfile.ZipFile('./static/test.zip', 'r')
    # Extract to static/picture directory
    archive.extractall('./static/picture')
    print('ZIP Extracted.')
    archive.close()

# Deleting files before getting new ones from the server.
def delete_files():
    files = glob.glob('static/picture/output/*.jpg', recursive=True)
    for f in files:
        os.remove(f)
    zip_path = './static/test.zip'
    os.remove(zip_path)
    print("All file deleted")

# Route deletes old files after clicking on the "Watch new video" button.
@app.route('/new', methods=['POST', 'GET'])
def new():
    delete_files()
    return redirect(url_for('get_video'))
    # return render_template('video.html')

# The route processes the page to view the video.
@app.route('/watch')
def index():
    def file_count(directory):
        files = os.listdir(directory)
        files.sort()
        return files
    s = file_count('static/picture/output/')
    z = ['/static/picture/output/'+ i +' ' for i in s]
    return render_template('index.html', s=s, z=z)

# Route creates a socket and receives the archive from the server, then unpacks it.
@app.route('/', methods=['POST', 'GET'])
def get_video():
    if request.method == 'POST':
        url = request.form['video_url']
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9090))
        sock.send(url.encode())
        file_name = sock.recv(100).decode()
        file_size = sock.recv(100).decode()

        # Open and write the file
        with open("./static/" + file_name, "wb") as file:
            c = 0
            # Starting the time capture
            start_time = time.time()

            # Will run the loop till all of the file is recived.
            while c <= int(file_size):
                data = sock.recv(1024)
                if not (data):
                    break
                file.write(data)
                c += len(data)
                s = int(file_size)
                size = os.path.getsize('./static/test.zip')

            # Ending the time capture.
            end_time = time.time()

        if c == s:
            unpack_zip()

        print("File transfer complete. Total time", end_time - start_time)

        sock.close()

        return redirect(url_for('index'))
    return render_template('video.html')


if __name__ == '__main__':
    app.run(debug=True)
