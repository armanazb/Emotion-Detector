function RunSentimentAnalysis() {
    var textToAnalyze = document.getElementById("textToAnalyze").value;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                document.getElementById("system_response").innerHTML = this.responseText;
            } else if (this.status == 400) {
                document.getElementById("system_response").innerHTML = "Invalid text! Please try again.";
            } else {
                document.getElementById("system_response").innerHTML = "Error: " + this.status;
            }
        }
    };
    xhttp.open("GET", "emotionDetector?textToAnalyze=" + encodeURIComponent(textToAnalyze), true);
    xhttp.send();
}
