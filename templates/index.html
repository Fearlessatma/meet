<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Live Speaker Diarization & Transcript</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
  <style>
    body {
      background-color: #f0f2f5;
      padding: 40px;
      font-family: 'Segoe UI', sans-serif;
    }

    .container {
      max-width: 800px;
      margin: auto;
      background: white;
      padding: 30px;
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    .btn {
      margin: 10px 10px 10px 0;
      min-width: 120px;
    }

    #transcript-box {
      height: 300px;
      overflow-y: auto;
      white-space: pre-wrap;
      background-color: #f8f9fa;
      border: 1px solid #ccc;
      border-radius: 10px;
      padding: 15px;
      font-family: monospace;
    }

    .title {
      font-size: 1.8rem;
      font-weight: bold;
      margin-bottom: 20px;
      color: #343a40;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="title">🎤 Live Speaker Diarization & Transcription</div>

    <button onclick="startRecording()" class="btn btn-success">Start</button>
    <button onclick="stopRecording()" class="btn btn-warning">Stop</button>
    <button onclick="clearFiles()" class="btn btn-danger">Clear</button>

    <!-- Alert placeholder -->
    <div id="alert-box" class="mt-3"></div>

    <!-- Transcript display -->
    <div id="transcript-box" class="mt-4"></div>
  </div>

  <script>
    function showAlert(message, type = 'success') {
      const alertBox = document.getElementById('alert-box');
      const alert = document.createElement('div');
      alert.className = `alert alert-${type} alert-dismissible fade show`;
      alert.role = 'alert';
      alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      `;
      alertBox.appendChild(alert);

      // Auto-dismiss after 3 seconds
      setTimeout(() => {
        alert.classList.remove('show');
        alert.classList.add('hide');
        setTimeout(() => alert.remove(), 500);
      }, 3000);
    }

    function startRecording() {
      fetch('/start-recording')
        .then(res => res.json())
        .then(data => {
          console.log(data);
          showAlert('🎙️ Recording started', 'success');
        });
    }

    function stopRecording() {
      fetch('/stop-recording')
        .then(res => res.json())
        .then(data => {
          console.log(data);
          showAlert('⏹️ Recording stopped', 'warning');
        });
    }

    function clearFiles() {
      fetch('/clear', { method: 'POST' })
        .then(response => response.text())
        .then(data => {
          alert(data);
          document.getElementById('transcript-box').innerText = '';
          showAlert('🗑️ Files cleared and transcript reset', 'danger');
        });
    }

    function updateTranscript() {
      fetch('/get-transcript')
        .then(response => response.json())
        .then(data => {
          let output = '';
          data.forEach(entry => {
            output += `🗣 ${entry.speaker}: ${entry.utterance}\n`;
          });
          const box = document.getElementById('transcript-box');
          box.innerText = output;
          box.scrollTop = box.scrollHeight;
        });
    }

    setInterval(updateTranscript, 5000); // Poll every 5 seconds
  </script>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
