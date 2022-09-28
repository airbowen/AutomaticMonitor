const option = {
  grid: {
    left: '3%',
    right: '5%',
    bottom: '3%',
    containLabel: true,
  },
  xAxis: {
    type: 'category',
    data: [],
    axisLabel: {
      text: '时间',
      fontSize: 5,
      rotate: 45,
    },
  },
  yAxis: {
    type: 'value',
    name: '频次',
    nameTextStyle: {
      fontSize: 6,
      fontWeight: 'bold',
      color: '#000',
    },
    axisLabel: {
      fontSize: 6,
    },
  },
  series: [
    {
      type: 'line',
      showSymbol: false,
      data: []
    }
  ],
}

const app = new Vue({
  el: '#app',
  data() {
    return {
      loading: true,
      len: 30,
      chart: null
    }
  },
  mounted() {
    this.chart = echarts.init(document.getElementById('chart'),null, { devicePixelRatio: 10 });
    this.getData(30);
  },
  methods: {
    getData(len) {
      this.loading = true;
      this.len = len; // 保存当前的分隔长度
      fetch(`http://localhost:5000/getData/${len}`)
        .then(res => res.json())
        .then(data => {
          const xList = []
          const yList = []
          data.forEach(item => {
            xList.push(item.time)
            yList.push(item.count)
          })
          option.xAxis.data = xList
          console.log(xList, yList)
          option.series[0].data = yList
          this.chart.setOption(option)
          this.loading = false
        })
    },
  }
})

app.$mount()