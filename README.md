# British Columbia Vaccine Card Decoder UI

## Disclaimer
The authors are in no way associated with the Government of British Columbia or with any health authority.
We make no guarantees as to the accuracy of the data extracted. Use this tool at
your own risk.

## Description
This is a simple web UI wrapper over jhaslam's [British Columbia Vaccine Card Decoder](https://github.com/jhaslam/bc_vaccine_card_decoder). See the original
for a discussion of the encoding system used in the vaccine cards.

Given an image of the vaccine card QR code, we invoke the [ZBar](http://zbar.sourceforge.net/) barcode reader to extract and serialize the code, then pass the result to the Vaccine Card Decoder library for parsing.

## Running the app locally

The application is packaged as a Docker image for ease of deployment. Assuming you have Docker running, you can build and run the tool locally like this:

```bash
docker build src -t decoder
docker run --rm -p 8080:8080 -ti decoder
```

Then open your browser to `http://localhost:8080/`.
