const running = "own_images/running_faster.gif";
const running_duration = 720;
const stopping = "own_images/emptying.gif";
const stopping_duration = 1890;
const empty = "own_images/empty.png";
const own = 2;

var ownCallback = null;

var machine1 = document.getElementById("machine_1");
var img1 = machine1.getElementsByTagName("img")[0];

var machineOwn = document.getElementById("own_machine");
var imgOwn = machineOwn.getElementsByTagName("img")[0];

var machine3 = document.getElementById("machine_3");
var img3 = machine3.getElementsByTagName("img")[0];

var machine4 = document.getElementById("machine_4");
var img4 = machine4.getElementsByTagName("img")[0];

var machines = [machineOwn, machine1, machineOwn, machine3, machine4];
var imgs = [imgOwn, img1, imgOwn, img3, img4];

var ownState = 0;
var onDuration = 0;

var popupShowing = 0;

var notIconTimeout = [];

setInterval(pollDb, 1000 );

for (var i = 1; i <= 4; i++) {
  if (i == own) continue;
  machines[i].schedule = createSchedule(i);
}

function createSchedule(number) {
  const obj = {};
  obj.delay = (2 + 6 * Math.random()) * 1000;
  obj.washing = Math.round(20 + 20 * Math.random()) * running_duration;
  obj.pausing = (10 + 10 * Math.random()) * 1000;  
  setTimeout(turnOn, obj.delay, number);
  return obj;
}

function turnOn(number) {
  imgs[number].src = running;
  showNotIcon(number);
  if (number != own) {
    setTimeout(turnOff, machines[number].schedule.washing, number);
  } else {
    if (ownCallback != null) {
      clearTimeout(ownCallback);
    }
    ownState = 1;
  }
}

function turnOff(number) {
  if (number != own || ownState == 1) {
    imgs[number].src = stopping;
    updateNotifications(number);
    fadeOutNotIcon(number);
    var cb = setTimeout(stop, stopping_duration, number);    
    if (number == own) {
      ownCallback = cb;
      ownState = 2;
    }
  }  
}

function stop(number) {
  imgs[number].src = empty;  
  if (number != own) {
    setTimeout(turnOn, machines[number].schedule.pausing, number);
  } else {
    ownState = 0;
  }
}

function updateNotifications(machine) {
  var http = new XMLHttpRequest();
  http.open("POST", "update_notifications.php", true);
  http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  var params = "machine=" + machine;
  http.send(params);
  http.onload = function() {
      // alert(http.responseText);
  }
}


function showNotIcon(number) {
  if(typeof notIconTimeout[number] !== "undefined"){
    clearTimeout(notIconTimeout[number]);
  }
  var icon = machines[number].getElementsByClassName("not_icon")[0];
  icon.style.display = "block";
  icon.style.opacity = "0";
  notIconTimeout[number] = setTimeout(fadeInNotIcon, 500, number);
}

function fadeInNotIcon(number) {
  var icon = machines[number].getElementsByClassName("not_icon")[0].style.opacity = "1";  
}

function fadeOutNotIcon(number) {
  var icon = machines[number].getElementsByClassName("not_icon")[0].style.opacity = "0";  
  notIconTimeout[number] = setTimeout(hideNotIcon, 500, number);
}

function hideNotIcon(number) {
  var icon = machines[number].getElementsByClassName("not_icon")[0].style.display = "none";  
}

String.prototype.toHHMMSS = function () {
    var sec_num = parseInt(this, 10); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+':'+minutes+':'+seconds;
}


function pollDb() {
  var xhttp; 
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var timestamp = this.responseText.split(" ")[0];
      var milliamps = parseInt(this.responseText.split(" ")[1]);  
      var age = Math.floor(Date.now() / 1000) - timestamp;
      if (milliamps > 1000) {
        document.getElementById("current").innerHTML = "Current: " + (milliamps/1000).toFixed(1) + "A";
        if (ownState != 1) {
          turnOn(own);
          document.getElementById("duration").innerHTML = "Now running.";
        } else {
          onDuration++;
          document.getElementById("duration").innerHTML = onDuration.toString().toHHMMSS();
        }        
      } else {
        onDuration = 0;
        document.getElementById("duration").innerHTML = "";
        document.getElementById("current").innerHTML = "";
        turnOff(own);
      }
      if (age < 5) {
        document.getElementById("own_machine").style.animation = "pulsate 1.5s ease-out infinite";
      } else {
        document.getElementById("own_machine").style.animation = "none";
      }
    }
  };
  xhttp.open("GET", "getresult.php", true);
  xhttp.send();
}

function showPopup(number) {
  document.getElementById("not_popup").style.visibility = 'visible';
  document.getElementById("ph_machine").innerHTML = 'machine ' + number.toString();
  document.getElementById("main").style.filter = "blur(8px)";
  var btn = document.getElementById("not_submit_btn");
  btn.style.webkitTransition = "0.5s";
  btn.style.oTransition = "0.5s";
  btn.style.transition = "0.5s";
  popupShowing = 1;
  if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    window.scrollTo(0, 0);
  }
}

function hidePopup() {
  document.getElementById("not_popup").style.visibility = 'hidden';
  document.getElementById("main").style.filter = "none";
  var btn = document.getElementById("not_submit_btn");
  btn.style.webkitTransition = "0s";
  btn.style.oTransition = "0s";
  btn.style.transition = "0s";
  var popup = document.getElementById("not_popup");
  popup.getElementsByTagName("input")["name"].value = "";
  popup.getElementsByTagName("input")["email"].value = "";
  popupShowing = 0;
}

document.onclick=check;
function check(e){
  var target = e && e.target;
  var popup = document.getElementById("not_popup");
  var not_icon = document.getElementById("not_icon");
  if (popupShowing == 1) {
    popupShowing = 2;
  } else if (popupShowing == 2 && !popup.contains(target) && popup.style.visibility == "visible") {
    hidePopup();
  }
}

function submitForm() {
  var http = new XMLHttpRequest();
  http.open("POST", "new_email_notification.php", true);
  http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  var popup = document.getElementById("not_popup");
  var name = popup.getElementsByTagName("input")["name"].value;
  var email = popup.getElementsByTagName("input")["email"].value;
  var machine = document.getElementById("ph_machine").innerHTML.split(" ")[1];
  var params = "name=" + name + "&email=" + email + "&machine=" + machine;
  hidePopup();
  http.send(params);
  http.onload = function() {
      // alert(http.responseText);
  }
}
