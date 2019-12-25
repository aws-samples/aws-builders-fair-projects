// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import AppRpi from './AppRpi'
import VueRouter from 'vue-router'

Vue.config.productionTip = false

/* eslint-disable no-new */
const config = {
	el: '#app',
	components: {App},
	template: '<App/>',
}

const routes = [
	{path: '/', component: App},
	{path: '/rpi', component: AppRpi},
]
const router = new VueRouter({
	mode: 'history',
	routes: routes,
})

new Vue({
	el:'#app',
	router,
	components: {
		'app-home' : App
	}
});
