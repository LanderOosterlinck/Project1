const verwerkTemperaturnen = function(data) {
	let htmlcode = '';
	let id = 0;
	for (gegevens of data) {
		datumentijd = gegevens.Dag;
		temp = gegevens.Temp;
		htmlcode += `<tr><td class="eerstetd">${datumentijd}</td><td>${temp}</td></tr>`;
	}

	domTemperatuurHolder.innerHTML = htmlcode;
};

const getTemperaturen = function() {
	handleData(
		`http://${window.location.hostname}:5000/api/v1/temperatuur`,
		verwerkTemperaturnen
	);
};

const init = function() {
	getTemperaturen();
	// getLichtsterkte();
	// getUV();
	// getLaatsteWaarden();
	domTemperatuurHolder = document.querySelector('.js-temperatuur');
	// domLichtsterkteHolder = document.querySelector('.js-lichtsterkte');
	// domUVsterkteHolder = document.querySelector('.js-uv');
	// domTempIndexHolder = document.querySelector('.js-graden');
	// domLichtIndexHolder = document.querySelector('.js-licht');
	// domUVIndexHodder = document.querySelector('.js-uvI');
};

document.addEventListener('DOMContentLoaded', init);