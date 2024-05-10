import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # Generate a temporary file path
    temp_file_path = tempfile.mktemp(suffix='.mp4')

    # Write video contents to the temp file
    with open(temp_file_path, 'wb') as tf:
        out = fs_videos.get(ObjectId(message["video_fid"]))
        tf.write(out.read())

    # Convert to audio
    audio = moviepy.editor.VideoFileClip(temp_file_path).audio

    # Write audio to a new temp file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    with open(tf_path, "rb") as f:
        data = f.read()
        fid = fs_mp3s.put(data)

    # Clean up temp files
    os.remove(temp_file_path)
    os.remove(tf_path)

    # Update message and publish
    message["mp3_fid"] = str(fid)
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        fs_mp3s.delete(fid)
        return "failed to publish message"
