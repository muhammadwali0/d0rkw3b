
import urllib.parse

def document_links(term):
    encoded = urllib.parse.quote_plus(term.strip())

    return {
        "Documents": {
            "PDF": f"https://www.google.com/search?q=ext%3Apdf+{encoded}",
            "DOC/DOCX": f"https://www.google.com/search?q=ext%3Adoc+OR+ext%3Adocx+{encoded}",
            "XLS/XLSX/CSV": f"https://www.google.com/search?q=ext%3Axls+OR+ext%3Axlsx+OR+ext%3Acsv+{encoded}",
            "PPT/PPTX/KEY": f"https://www.google.com/search?q=ext%3Appt+OR+ext%3Apptx+OR+ext%3Akey+{encoded}",
            "TXT/RTF/XML": f"https://www.google.com/search?q=ext%3Atxt+OR+ext%3Artf+OR+ext%3Axml+{encoded}",
            "ODT/ODS/ODP": f"https://www.google.com/search?q=ext%3Aodt+OR+ext%3Aods+OR+ext%3Aodp+{encoded}",
            "ZIP/RAR/7Z": f"https://www.google.com/search?q=ext%3Azip+OR+ext%3Arar+OR+ext%3A7z+{encoded}",
            "JPG/JPEG/PNG": f"https://www.google.com/search?q=ext:jpg+OR+ext:jpeg+OR+ext:png+{encoded}&udm=2",
            "MPG/MP4": f"https://www.google.com/search?q=ext%3Ampg+OR+ext%3Ampeg+OR+ext%3Amp4+{encoded}",
            "MP3/WAV": f"https://www.google.com/search?q=ext%3Amp3+OR+ext%3Awav+OR+ext%3Aflac+{encoded}",
            "Google Docs": f"https://www.google.com/search?q=site%3Adocs.google.com+{encoded}",
            "Google Drive": f"https://www.google.com/search?q=site%3Adrive.google.com+{encoded}",
            "Google API": f"https://www.google.com/search?q=site%3Astorage.googleapis.com+{encoded}",
            "MS Docs": f"https://www.google.com/search?q=site%3Adocs.microsoft.com+{encoded}",
            "Amazon AWS": f"https://www.google.com/search?q=site%3Aamazonaws.com+{encoded}",
            "CloudFront": f"https://www.google.com/search?q=site%3Acloudfront.net+{encoded}",
            "Refseek": f"https://www.refseek.com/documents?q={encoded}",
            "Core": f"https://core.ac.uk/search/?q={encoded}",
            "GrayHatWarfare": f"https://buckets.grayhatwarfare.com/files?page=1&keywords={encoded}",
            "SlideShare": f"https://www.google.com/search?q=site%3Aslideshare.net+{encoded}",
            "Prezi": f"https://www.google.com/search?q=site%3Aprezi.com+{encoded}",
            "ISSUU": f"https://www.google.com/search?q=site%3Aissuu.com+{encoded}",
            "Powershow": f"https://www.powershow.com/search/presentations/ppt/{encoded}",
            "Slide Bean": f"https://www.google.com/search?q=site%3Aslidebean.com+{encoded}",
            "Scribd": f"https://www.google.com/search?q=site%3Ascribd.com+{encoded}",
            "PDF Drive": f"https://welib.org/?q={encoded}",
            "Wikileaks": f"https://search.wikileaks.org/?query={encoded}&exact_phrase=&any_of=&exclude_words=&document_date_start=&document_date_end=&released_date_start=&released_date_end=&new_search=True&order_by=most_relevant#results",
            "Archive.org": f"https://archive.org/search?query={encoded}&sin=TXT",
            "Google Books": f"https://www.google.com/search?tbm=bks&q={encoded}"
        }
    }

