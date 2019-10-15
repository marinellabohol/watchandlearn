	var score = 0;

	var vocabScore = 0;
	var readingScore = 0;
	var writingScore = 0;
	var grammarScore = 0;


	var vocabSlider = document.getElementById("vocabulary");
	var vocabOutput = document.getElementById("vocabText");
	vocabOutput.innerHTML = vocabSlider.value;

	vocabSlider.oninput = function() {
	  vocabScore = this.value;
	  vocabOutput.innerHTML = vocabScore;
	  score = score + vocabScore;
	}
	var readingSlider = document.getElementById("reading");
	var readingOutput = document.getElementById("readingText");
	readingOutput.innerHTML = readingSlider.value;

	readingSlider.oninput = function() {
	  readingScore = this.value;
	  readingOutput.innerHTML = readingScore;
	  score = score + readingScore;
	}
	var writingSlider = document.getElementById("writing");
	var writingOutput = document.getElementById("writingText");
	writingOutput.innerHTML = writingSlider.value;

	writingSlider.oninput = function() {
	  writingScore = this.value;
	  writingOutput.innerHTML = writingScore;
	  score = score + writingScore;
	}
	var grammarSlider = document.getElementById("grammar");
	var grammarOutput = document.getElementById("grammarText");
	grammarOutput.innerHTML = grammarSlider.value;

	grammarSlider.oninput = function() {
	  grammarScore = this.value;
	  grammarOutput.innerHTML = grammarScore;
	  score = score + grammarScore;
	}

	console.log(vocabScore);
	console.log(readingScore);
	console.log(writingScore);
	console.log(grammarScore);
	
