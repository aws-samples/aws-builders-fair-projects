<template>
	<div id="chart2">
		<apexchart ref='chart' type=line height=200 :options="chartOptionsChart"/>
	</div>
</template>

<script>
    import Vue from 'vue'
    import VueApexCharts from 'vue-apexcharts'

    Vue.use(VueApexCharts)
    Vue.component('apexchart', VueApexCharts)
    import {chartExportComponents} from '../configs/chart/chartComponents'

    export default chartExportComponents

</script>
<style scoped>
</style>
