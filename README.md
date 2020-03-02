# Indonesian Driving License OCR Service (API)

An OCR API service for a cropped Indonesian Driving License
- Extracts all text data

### <b> Third party library used:</b> 
kraken, CV, Tesseract


### <b> Instructions: </b>
1. Install requirements in requirements.txt
2. Run home.py for API testing

### <b>Output:</b>
```
json = {
        "message"       : "OCR Success",
        "success"       : True,
        "documentType"  : "SIMprocessed",
        "data"          : {
            "Nama" : nama,
            "Alamat": alamat,
            "JenisKelamin": kelamin,
            "TempatLahir" : teL,
            "TanggalLahir": taL,
            "Tinggi": tinggi,
            "Pekerjaan": pekerjaan,
            "NoSIM": noSIM,
            "JenisSIM": jenisSim,
            "mb":mb
        },
        "img"           : {
            "sim": filename,
        }
    }
```
