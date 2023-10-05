let url = `ws://${window.location.host}/ws/socket-server/`
const chatSocket = new WebSocket(url)  // WebSocket object
const chat_room_id = document.getElementById('chat-room-id').textContent.trim();
let currentUsername = document.currentScript.getAttribute('data-username');

chatSocket.onmessage = function(e) 
{
  let data = JSON.parse(e.data) // used to convert the JSON string into a JavaScript object.
  if(data.type === 'chat')
  {
    let messages = document.getElementById('messages')
    let messageItem = document.createElement('li');
   
    if (data.username != currentUsername ) 
    {
    messages.insertAdjacentHTML('beforeend', ` 
    <li class="clearfix">
                        <div class="message-data">
                          ${data.username}
                            <span class="message-data-time">${data.timestamp}</span>
                            <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="avatar">
                        </div>
                        <div class="message my-message">  ${data.message}</div>
                    </li>                   
              `)
  }
  else
  {
    messages.insertAdjacentHTML('beforeend', `
    <li class="clearfix">
                        <div class="message-data pull-right">                          
                            <span class="message-data-time">${data.timestamp}</span>
                            Me
                        </div>
                      </br>
                    </br>       
                        <div class="message other-message float-right">${data.message}</div>                                    
                    </li>
   `)
  }
  
}
  else if (data.type === 'image')
  {
    let messages = document.getElementById('messages');
    let messageItem = document.createElement('li');
    if (data.username !== currentUsername) 
    {
      messages.insertAdjacentHTML('beforeend', `
        <li class="clearfix">
          <div class="message-data">
            ${data.username}
            <span class="message-data-time">${data.timestamp}</span>
            <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="avatar">
          </div>
          <div class="message my-message">
            <img src="${data.image}" alt="image" style="max-width: 200px; max-height: 200px;" >
          </div>
        </li>
      `);
    } 
    else 
    {
      messages.insertAdjacentHTML('beforeend', `
        <li class="clearfix">
          <div class="message-data pull-right">
            <span class="message-data-time">${data.timestamp}</span>
            Me
          </div>
          </br>
          </br>
          <div class="message other-message float-right">
            <img src="${data.image}" alt="image" style="max-width: 200px; max-height: 200px;">
          </div>
        </li>
      `);
    }
}
else if (data.type === 'audio')
{
    console.log('audio in websocket')
    let messages = document.getElementById('messages');
    let messageItem = document.createElement('li');
    if (data.username !== currentUsername) 
    {
      
      messages.insertAdjacentHTML('beforeend', `
        <li class="clearfix">
          <div class="message-data">
            ${data.username}
            <span class="message-data-time">${data.timestamp}</span>
          </div>
          <div class="message my-message">
        
          <audio controls>       
          <source src="${ data.audioURL }" type="audio/webm">
          Your browser does not support the audio element.
        </audio>
        </div>
    </div>
        </li>
      `);
    } 
    else 
    {
     
      messages.insertAdjacentHTML('beforeend', `
        <li class="clearfix">
          <div class="message-data pull-right">
            <span class="message-data-time">${data.timestamp}</span>
            Me
        </div>
        
        </br>
        </br>
        <div class="message other-message float-right">
          <audio controls>
          <source src="${ data.audioURL }" type="audio/webm">
          Your browser does not support the audio element.
        </audio>
        </div>
        </li>
      `);
    
}
}
document.getElementById('messages').scrollTop = messages.scrollHeight;

  }

document.getElementById('send-image-btn').addEventListener('click', (e)=> {
e.preventDefault()
const fileInput = document.getElementById('image-input');
if (fileInput.files.length > 0) {
  const file = fileInput.files[0];

  // Read the image file as a data URL
  const reader = new FileReader();
  reader.onload = function(e) {
    const imageDataUrl = e.target.result;
    const message = 
    {
      type: 'image',
      chat_room_id: chat_room_id,
      image: imageDataUrl,
    };
    chatSocket.send(JSON.stringify(message));
  };
  reader.readAsDataURL(file);
}
else{
  let form = document.getElementById('form')
  e.preventDefault()
  let message = document.getElementsByClassName('chat-form')[0].message.value
  chatSocket.send(JSON.stringify(
    {
    'type':'chat',
    'message':message,
    'chat_room_id': chat_room_id,
    'username': currentUsername
  } 
  )
  )
  form.reset() 

}
}
);

  // Add event listener to the record button
const audioButton = document.getElementById('audio-input-btn');
audioButton.addEventListener('click', function(event) {
  event.preventDefault(); 
  sendRecordedAudio();
});
// audioButton.addEventListener('click',sendRecordedAudio);

const recordButton = document.getElementById('record-button');
recordButton.addEventListener('click', startRecording);

const stopButton = document.getElementById('stop-button');
stopButton.addEventListener('click', stopRecording);

const playButton = document.getElementById('play-button');
playButton.addEventListener('click', playRecording);

let mediaRecorder; // MediaRecorder instance
let chunks = []; // Array to store recorded audio chunks
let audioElement; // Audio element for playback
let temp = null;
let recordedAudioURL; 
let blob;
// Event listener for record button click
function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then((stream) => {
      temp=stream;
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.addEventListener('start', onRecordingStart);
      mediaRecorder.addEventListener('stop', onRecordingStop);
      mediaRecorder.addEventListener('dataavailable', onRecordingDataAvailable);

      mediaRecorder.start();
      recordButton.disabled = true; // Disable the record button
      stopButton.disabled = false; // Enable the stop button
    })
    .catch((error) => {
      console.error('Error accessing microphone:', error);
    });
}

// Event listener for recording start
function onRecordingStart() {
  console.log('Recording started');
  console.log(mediaRecorder.state)
  recordButton.disabled = true; // Disable the record button
  stopButton.disabled = false; // Enable the stop button
}

// Event listener for recording stop
function onRecordingStop() {
  console.log('Recording stopped');
  console.log(mediaRecorder.state)
  temp.getTracks()[0].stop()
  recordButton.disabled = false; // Enable the record button
  stopButton.disabled = true; // Disable the stop button

  recordedAudioURL = audioElement.src;
 
}

// Event listener for data available during recording
function onRecordingDataAvailable(event) {
  chunks = []; // Reset the chunks array
  chunks.push(event.data);
  createAudioElement();
  console.log('adding chunk',event.data);
}

// Function to stop the recording
function stopRecording() 
{
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
    recordButton.disabled = false; // Enable the record button
    stopButton.disabled = true; // Disable the stop button

     // Create audio element for playback
  }
}

// Function to create an audio element and set the recorded audio as the source
function createAudioElement() {
 
  blob = new Blob(chunks, { type: 'audio/webm' });
  const audioURL = window.URL.createObjectURL(blob);
  audioElement = document.createElement('audio');
  audioElement.controls = true;
  audioElement.src = audioURL;
  // audioElement = audioURL
}

// Function to play the recorded audio
function playRecording() {
  if (audioElement) {
    
    audioElement.play();
  }
}

function convertBlobToJson(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = function () {
      const dataURL = reader.result;
      const jsonPayload = JSON.stringify({
        type: 'audio',
        audioURL: dataURL,
      });
      resolve(jsonPayload);
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

function sendRecordedAudio() {
  console.log('sendRecordedAudio function is running');
  if (recordedAudioURL) {
    convertBlobToJson(blob)
      .then(jsonPayload => {
        const parsedPayload = JSON.parse(jsonPayload);
        parsedPayload.chat_room_id = chat_room_id;
        chatSocket.send(JSON.stringify(parsedPayload));
      })
      .catch(error => {
        console.error('Error converting Blob to JSON:', error);
      });

  }
}


