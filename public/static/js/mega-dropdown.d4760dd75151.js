
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
/******/ 	return __webpack_require__(__webpack_require__.s = "./js/mega-dropdown.es6");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./js/mega-dropdown.es6":
/*!******************************!*\
  !*** ./js/mega-dropdown.es6 ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
eval("\n\nObject.defineProperty(exports, \"__esModule\", {\n  value: true\n});\n\nvar _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if (\"value\" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();\n\nfunction _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError(\"Cannot call a class as a function\"); } }\n\nvar TIMEOUT = 150;\n\nvar MegaDropdown = function () {\n  function MegaDropdown(element) {\n    var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};\n\n    _classCallCheck(this, MegaDropdown);\n\n    this._onHover = options.trigger === 'hover' || element.getAttribute('data-trigger') === 'hover';\n\n    this._container = this._findParent(element, 'mega-dropdown');\n    if (!this._container) return;\n\n    this._menu = this._container.querySelector('.dropdown-toggle ~ .dropdown-menu');\n    if (!this._menu) return;\n\n    element.setAttribute('aria-expanded', 'false');\n\n    this._el = element;\n    this._bindEvents();\n  }\n\n  _createClass(MegaDropdown, [{\n    key: 'open',\n    value: function open() {\n      if (this._timeout) {\n        clearTimeout(this._timeout);\n        this._timeout = null;\n      }\n      if (this._focusTimeout) {\n        clearTimeout(this._focusTimeout);\n        this._focusTimeout = null;\n      }\n\n      if (this._el.getAttribute('aria-expanded') !== 'true') {\n        this._triggerEvent('show');\n        this._container.classList.add('show');\n        this._menu.classList.add('show');\n        this._el.setAttribute('aria-expanded', 'true');\n        this._el.focus();\n        this._triggerEvent('shown');\n      }\n    }\n  }, {\n    key: 'close',\n    value: function close(force) {\n      var _this = this;\n\n      if (this._timeout) {\n        clearTimeout(this._timeout);\n        this._timeout = null;\n      }\n      if (this._focusTimeout) {\n        clearTimeout(this._focusTimeout);\n        this._focusTimeout = null;\n      }\n\n      if (this._onHover && !force) {\n        this._timeout = setTimeout(function () {\n          if (_this._timeout) {\n            clearTimeout(_this._timeout);\n            _this._timeout = null;\n          }\n          _this._close();\n        }, TIMEOUT);\n      } else {\n        this._close();\n      }\n    }\n  }, {\n    key: 'toggle',\n    value: function toggle() {\n      this._el.getAttribute('aria-expanded') === 'true' ? this.close(true) : this.open();\n    }\n  }, {\n    key: 'destroy',\n    value: function destroy() {\n      this._unbindEvents();\n      this._el = null;\n\n      if (this._timeout) {\n        clearTimeout(this._timeout);\n        this._timeout = null;\n      }\n\n      if (this._focusTimeout) {\n        clearTimeout(this._focusTimeout);\n        this._focusTimeout = null;\n      }\n    }\n  }, {\n    key: '_close',\n    value: function _close() {\n      if (this._el.getAttribute('aria-expanded') === 'true') {\n        this._triggerEvent('hide');\n        this._container.classList.remove('show');\n        this._menu.classList.remove('show');\n        this._el.setAttribute('aria-expanded', 'false');\n        this._triggerEvent('hidden');\n      }\n    }\n  }, {\n    key: '_bindEvents',\n    value: function _bindEvents() {\n      var _this2 = this;\n\n      this._elClickEvnt = function (e) {\n        e.preventDefault();\n        _this2.toggle();\n      };\n      this._el.addEventListener('click', this._elClickEvnt);\n\n      this._bodyClickEvnt = function (e) {\n        if (!_this2._container.contains(e.target) && _this2._container.classList.contains('show')) {\n          _this2.close(true);\n        }\n      };\n      document.body.addEventListener('click', this._bodyClickEvnt, true);\n\n      this._menuClickEvnt = function (e) {\n        if (e.target.classList.contains('mega-link')) {\n          _this2.close(true);\n        }\n      };\n      this._menu.addEventListener('click', this._menuClickEvnt, true);\n\n      this._focusoutEvnt = function (e) {\n        if (_this2._focusTimeout) {\n          clearTimeout(_this2._focusTimeout);\n          _this2._focusTimeout = null;\n        }\n\n        if (_this2._el.getAttribute('aria-expanded') !== 'true') return;\n\n        _this2._focusTimeout = setTimeout(function () {\n          if (document.activeElement.tagName.toUpperCase() !== 'BODY' && _this2._findParent(document.activeElement, 'mega-dropdown') !== _this2._container) {\n            _this2.close(true);\n          }\n        }, 100);\n      };\n      this._container.addEventListener('focusout', this._focusoutEvnt, true);\n\n      if (this._onHover) {\n        this._enterEvnt = function (e) {\n          if (window.getComputedStyle(_this2._menu, null).getPropertyValue('position') === 'static') return;\n          _this2.open();\n        };\n        this._leaveEvnt = function (e) {\n          if (window.getComputedStyle(_this2._menu, null).getPropertyValue('position') === 'static') return;\n          _this2.close();\n        };\n\n        this._el.addEventListener('mouseenter', this._enterEvnt);\n        this._menu.addEventListener('mouseenter', this._enterEvnt);\n        this._el.addEventListener('mouseleave', this._leaveEvnt);\n        this._menu.addEventListener('mouseleave', this._leaveEvnt);\n      }\n    }\n  }, {\n    key: '_unbindEvents',\n    value: function _unbindEvents() {\n      if (this._elClickEvnt) {\n        this._el.removeEventListener('click', this._elClickEvnt);\n        this._elClickEvnt = null;\n      }\n      if (this._bodyClickEvnt) {\n        document.body.removeEventListener('click', this._bodyClickEvnt, true);\n        this._bodyClickEvnt = null;\n      }\n      if (this._menuClickEvnt) {\n        this._menu.removeEventListener('click', this._menuClickEvnt, true);\n        this._menuClickEvnt = null;\n      }\n      if (this._focusoutEvnt) {\n        this._container.removeEventListener('focusout', this._focusoutEvnt, true);\n        this._focusoutEvnt = null;\n      }\n      if (this._enterEvnt) {\n        this._el.removeEventListener('mouseenter', this._enterEvnt);\n        this._menu.removeEventListener('mouseenter', this._enterEvnt);\n        this._enterEvnt = null;\n      }\n      if (this._leaveEvnt) {\n        this._el.removeEventListener('mouseleave', this._leaveEvnt);\n        this._menu.removeEventListener('mouseleave', this._leaveEvnt);\n        this._leaveEvnt = null;\n      }\n    }\n  }, {\n    key: '_findParent',\n    value: function _findParent(el, cls) {\n      if (el.tagName.toUpperCase() === 'BODY') return null;\n      el = el.parentNode;\n      while (el.tagName.toUpperCase() !== 'BODY' && !el.classList.contains(cls)) {\n        el = el.parentNode;\n      }\n      return el.tagName.toUpperCase() !== 'BODY' ? el : null;\n    }\n  }, {\n    key: '_triggerEvent',\n    value: function _triggerEvent(event) {\n      if (document.createEvent) {\n        var customEvent = void 0;\n\n        if (typeof Event === 'function') {\n          customEvent = new Event(event);\n        } else {\n          customEvent = document.createEvent('Event');\n          customEvent.initEvent(event, false, true);\n        }\n\n        this._container.dispatchEvent(customEvent);\n      } else {\n        this._container.fireEvent('on' + event, document.createEventObject());\n      }\n    }\n  }]);\n\n  return MegaDropdown;\n}();\n\nexports.MegaDropdown = MegaDropdown;\n\n//# sourceURL=webpack:///./js/mega-dropdown.es6?");

/***/ })

/******/ });
});;