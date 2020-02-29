
(function(r,f) {
	var a=f();
	if(typeof a!=='object')return;
	var e=[typeof module==='object'&&typeof module.exports==='object'?module.exports:null,typeof window!=='undefined'?window:null,r&&r!==window?r:null];
	for(var i in a){e[0]&&(e[0][i]=a[i]);e[1]&&i!=='__esModule'&&(e[1][i] = a[i]);e[2]&&(e[2][i]=a[i]);}
})(this,function(){
	return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./js/landing.es6");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./js/landing.es6":
/*!************************!*\
  !*** ./js/landing.es6 ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
eval("\n\n$(function () {\n    var swiperWithPagination = new Swiper('#swiper-with-pagination', {\n        pagination: {\n            el: '.swiper-pagination',\n            clickable: true\n        }\n    });\n\n    // Wrap charts\n    $('.chartjs').each(function () {\n        $(this).wrap($('<div style=\"height:' + this.getAttribute('height') + 'px\"></div>'));\n    });\n    var pieChart = new Chart(document.getElementById('chart-pie').getContext(\"2d\"), {\n        type: 'pie',\n        data: {\n            labels: ['Пройдено', 'Не пройдено'],\n            datasets: [{\n                data: [5, 15],\n                backgroundColor: ['#F2F2F2', '#F26722'],\n                hoverBackgroundColor: ['#F2F2F2', '#F26722']\n            }]\n        },\n\n        // Demo\n        options: {\n            responsive: true,\n            maintainAspectRatio: false,\n            legend: {\n                display: false\n            },\n            tooltips: {\n                enabled: false\n            }\n        }\n    });\n});\n\n//# sourceURL=webpack:///./js/landing.es6?");

/***/ })

/******/ });
});;