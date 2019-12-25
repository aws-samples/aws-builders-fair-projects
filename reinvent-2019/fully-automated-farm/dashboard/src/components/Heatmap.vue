<template>
	<div id='chart'>
		<apexchart ref='heatmap' type=heatmap height=200 :options='chartOptionsHeatMap'/>
	</div>
</template>

<script>
    import Vue from 'vue'
    import VueApexCharts from 'vue-apexcharts'

    Vue.use(VueApexCharts)
    Vue.component('apexchart', VueApexCharts)

    import {heatmapExportComponents} from '../configs/heatmap/heatmapComponents'

    export default heatmapExportComponents
</script>

<style scoped>
	h1,
	h2 {
		font-weight: normal;
	}

	ul {
		list-style-type: none;
		padding: 0;
	}

	li {
		display: inline-block;
		margin: 0 10px;
	}

	a {
		color: #42b983;
	}
</style>
