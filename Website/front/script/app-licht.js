const verwerkLichtsterkte = function(data) {
	let htmlcode2 = '';
	for (gegevens of data) {
		datumentijd = gegevens.Dag;
		licht = gegevens.licht;
		htmlcode2 += `<tr><td class="eerstetd">${datumentijd}</td><td>${licht}</td></tr>`;
	}

	domLichtsterkteHolder.innerHTML = htmlcode2;
};

const getLichtsterkte = function() {
	handleData(
		`http://${window.location.hostname}:5000/api/v1/lichtsterkte`,
		verwerkLichtsterkte
	);
};

const init = function() {
	// 	getTemperaturen();
	getLichtsterkte();
	// 	getUV();
	//  getLaatsteWaarden();
	//  listenToOpslaan();
	//	domTemperatuurHolder = document.querySelector('.js-temperatuur');
	domLichtsterkteHolder = document.querySelector('.js-lichtsterkte');
	// 	domUVsterkteHolder = document.querySelector('.js-uv');
	//  domTempIndexHolder = document.querySelector('.js-graden');
	//  domLichtIndexHolder = document.querySelector('.js-licht');
	//  domUVIndexHodder = document.querySelector('.js-uvI');
};

document.addEventListener('DOMContentLoaded', init);