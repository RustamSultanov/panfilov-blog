import * as mdc from 'material-components-web';
mdc.autoInit();
import {MDCDrawer} from "@material/drawer";
import {MDCTopAppBar} from "@material/top-app-bar";
const drawer = MDCDrawer.attachTo(document.querySelector('.mdc-drawer'));
const topAppBar = MDCTopAppBar.attachTo(document.getElementById('top-app-bar'));
//topAppBar.setScrollTarget(document.getElementById('main-content'));
topAppBar.listen('MDCTopAppBar:nav', () => {
    drawer.open = !drawer.open;
});
import Glide from '@glidejs/glide';
new Glide('.glide', {
  type: 'carousel',
  perView: 1
}).mount();