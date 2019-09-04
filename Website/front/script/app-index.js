let domTemperatuurHolder, domLichtsterkteHolder, domUVsterkteHolder;
let domTempIndexHolder, domLichtIndexHolder, domUVIndexHodder;
let domGewildeTempHodler;

const verwerkOpslaan = function(json) {
	console.log(json);
};

const listenToOpslaan = function() {
	document.querySelector('.js-button').addEventListener('click', function() {
		let currentWaarde = parseInt(
			document.querySelector('.js-waarde').value
		);
		handleData(
			`http://${window.location.hostname}:5000/api/v1/meting/log/${currentWaarde}`,
			verwerkOpslaan,
			'PUT'
		);
	});
};

window.onload = function() {
	setInterval(getDataSensoren, 1800);
};

const VerwerkSensorData = function(json) {
	console.log(json);
};

const getDataSensoren = function() {
	handleData(
		`http://${window.location.hostname}:5000/api/v1/meting`,
		VerwerkSensorData,
		'PUT'
	);
};

const verwerkIndex = function(data) {
	let htmlcode4 = '';
	let htmlcode5 = '';
	let htmlcode6 = '';
	temp = data[0].temp;
	licht = data[1].licht;
	uv = data[2].uv;

	htmlcode4 = `<h1 class="graden js-graden">${temp}°C</h1>`;
	htmlcode5 = `<h1 class="graden js-licht">${licht}%</h1>`;
	htmlcode6 = `<h1 class="graden js-uv">${uv}nm</h1>`;

	domTempIndexHolder.innerHTML = htmlcode4;
	domLichtIndexHolder.innerHTML = htmlcode5;
	domUVIndexHodder.innerHTML = htmlcode6;
};

const getLaatsteWaarden = function() {
	handleData(
		`http://${window.location.hostname}:5000/api/v1/index`,
		verwerkIndex
	);
};

// const verwerkUV = function(data) {
// 	let htmlcode3 = '';
// 	for (gegevens of data) {
// 		datumentijd = gegevens.Dag;
// 		uv = gegevens.uv;
// 		htmlcode3 += `<tr><td class="eerstetd">${datumentijd}</td><td>${uv}</td></tr>`;
// 	}

// 	domUVsterkteHolder.innerHTML = htmlcode3;
// };

// const getUV = function() {
// 	handleData(`http://${window.location.hostname}:5000/api/v1/uv`, verwerkUV);
// };

// const verwerkLichtsterkte = function(data) {
// 	let htmlcode2 = '';
// 	for (gegevens of data) {
// 		datumentijd = gegevens.Dag;
// 		licht = gegevens.licht;
// 		htmlcode2 += `<tr><td class="eerstetd">${datumentijd}</td><td>${licht}</td></tr>`;
// 	}

// 	domLichtsterkteHolder.innerHTML = htmlcode2;
// };

// const getLichtsterkte = function() {
// 	handleData(
// 		`http://${window.location.hostname}:5000/api/v1/lichtsterkte`,
// 		verwerkLichtsterkte
// 	);
// };

// const verwerkTemperaturnen = function(data) {
// 	let htmlcode = '';
// 	let id = 0;
// 	for (gegevens of data) {
// 		datumentijd = gegevens.Dag;
// 		temp = gegevens.Temp;
// 		htmlcode += `<tr><td class="eerstetd">${datumentijd}</td><td>${temp}</td></tr>`;
// 	}

// 	domTemperatuurHolder.innerHTML = htmlcode;
// };

// const getTemperaturen = function() {
// 	handleData(
// 		`http://${window.location.hostname}:5000/api/v1/temperatuur`,
// 		verwerkTemperaturnen
// 	);
// };

const init = function() {
	// 	getTemperaturen();
	// 	getLichtsterkte();
	// 	getUV();
	getLaatsteWaarden();
	listenToOpslaan();
	// 	domTemperatuurHolder = document.querySelector('.js-temperatuur');
	// 	domLichtsterkteHolder = document.querySelector('.js-lichtsterkte');
	// 	domUVsterkteHolder = document.querySelector('.js-uv');
	domTempIndexHolder = document.querySelector('.js-graden');
	domLichtIndexHolder = document.querySelector('.js-licht');
	domUVIndexHodder = document.querySelector('.js-uvI');
};

document.addEventListener('DOMContentLoaded', init);
