from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from os import listdir
from os.path import isfile, join
from scripts.clean import clean
from scripts.segment import segment
import sys
import shutil


if __name__ == "__main__":
    # bookfile takes in the file location, bookname takes the name of the book.
    bookname = sys.argv[1]

    # Only include the mp3 files
    mp3files = [f for f in listdir("./public/uploads/{}/".format(bookname)) if isfile(join("./public/uploads/{}/".format(bookname), f)) and f.endswith(".mp3")]

    # Clean the book before segmenting
    # Combs the book for headers and sentences
    clean(bookname)

    # Uses a script to segment the book
    # Outputs the segments to a seperate folder located in ./output/bookname/
    segment(bookname)

    # Only include the text files that end in html
    segments = [f for f in listdir("./public/uploads/{}/segments/".format(bookname)) if isfile(join("./public/uploads/{}/segments/".format(bookname), f)) and f.endswith(".html")]

    # There needs to be the same number of mp3 files as there are segment files. 1 to 1 ratio!
    print("mp3 files: {}, segments: {}".format(len(mp3files), len(segments)))

    # Run through each mp3 file and book segment
    for i, mp3 in enumerate(mp3files):
        # Setup config string & absolute file path for audio/text/syncfile
        
        # Changed "task_adjust_boundary_nonspeech_min=1.0|task_adjust_boundary_nonspeech_string=REMOVE" from config string may be useful..

        config_string = u"task_language=isl|is_text_type=unparsed|os_task_file_format=smil|os_task_file_smil_audio_ref={}|os_task_file_smil_page_ref={}.html".format(mp3, bookname)
        # Create Task
        task = Task(config_string=config_string)
        task.audio_file_path_absolute = u"./public/uploads/{}/{}".format(bookname, mp3)
        task.text_file_path_absolute = u"./public/uploads/{}/segments/b{}.html".format(bookname, i+1)
        # Each smil file is named s + number with leading zeros
        task.sync_map_file_path_absolute = u"./public/output/{}/s{}.smil".format(bookname, str(i+1).zfill(3))

        # Debug print
        print("Running task nr: {}/{}".format(i+1, len(mp3files)))

        # Execute Task to output path
        ExecuteTask(task).execute()
        task.output_sync_map_file()

    shutil.make_archive("./public/output/{}".format(bookname), 'zip', "./public/output/{}".format(bookname))
    print("Done")