curl -X POST http://localhost:5000/test \
  -F "image=@test.jpg" \
  -F "brightness=1.3" \
  -F "contrast=0.8" \
  -o response.json
