const verwerkUV = function(data) {
	let htmlcode3 = '';
	for (gegevens of data) {
		datumentijd = gegevens.Dag;
		uv = gegevens.uv;
		htmlcode3 += `<tr><td class="eerstetd">${datumentijd}</td><td>${uv}</td></tr>`;
	}

	domUVsterkteHolder.innerHTML = htmlcode3;
};

const getUV = function() {
	handleData(`http://${window.location.hostname}:5000/api/v1/uv`, verwerkUV);
};


const init = function() {
	// getTemperaturen();
	// getLichtsterkte();
	getUV();
	// getLaatsteWaarden();
	// domTemperatuurHolder = document.querySelector('.js-temperatuur');
	// domLichtsterkteHolder = document.querySelector('.js-lichtsterkte');
	domUVsterkteHolder = document.querySelector('.js-uv');
	// domTempIndexHolder = document.querySelector('.js-graden');
	// domLichtIndexHolder = document.querySelector('.js-licht');
	// domUVIndexHodder = document.querySelector('.js-uvI');
};

document.addEventListener('DOMContentLoaded', init);