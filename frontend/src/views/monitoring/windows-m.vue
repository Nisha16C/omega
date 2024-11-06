<template>
  <div>
    
    <n-card title=""  size="small">
      <n-h2 prefix="bar" >
      <n-text type="primary">
        Windows Monitoring Dashboards      </n-text>
    </n-h2>
      <!-- Card Content -->
    </n-card>
    <!-- Dropdown Section -->
    <n-card>
    <div class="dropdown-container">

      <!-- Job Dropdown -->
      <div class="dropdown-item">
        <div class="label-box">Job</div>
        <n-select v-model="selectedJob" :options="jobOptions" placeholder="Select Job" style="width: 200px;"
          @update:value="onJobSelect"></n-select>
      </div>

      <!-- Host Dropdown -->
      <div class="dropdown-item">
        <div class="label-box">host</div>
        <n-select v-model="selectedHost" :options="filteredHostOptions" placeholder="Select Host" style="width: 200px;"
          @update:value="onHostSelect"></n-select>
      </div>
    </div>
  </n-card>

    <!-- Gauge Chart Section for CPU Usage and Sys Load -->
    <n-card>
      <div class="panel-row">
        <!-- Panel 1: CPU Usage -->
        <div class="panel-container">
          <div class="panel-title">CPU Usage</div> <!-- Panel Title -->
          <div ref="gaugeChartSysLoad" class="gauge-chart"></div>
        </div>

        
        <div class="panel-container">
          <div class="panel-title">Hard Disk Usage</div> <!-- Panel Title -->
          <div ref="gaugeChartCpu" class="gauge-chart"></div>
        </div>

        <!-- Panel 2: Sys Load -->


        <!-- Panel 3: RAM Load -->
        <div class="panel-container">
          <div class="panel-title">Memory Usage Load</div> <!-- Panel Title -->
          <div ref="gaugeChartRamLoad" class="gauge-chart"></div>
        </div>

        <!-- Panel 4: Root fs Used -->
        <div class="panel-container">
          <div class="panel-title">Disk Usage</div> <!-- Panel Title -->
          <div ref="gaugeChartRootUsed" class="gauge-chart"></div>
        </div>
      </div>
    </n-card>
    <n-card>
      <div class="panel-row">
        <div class="panel-container">
          <div class="panel-title">CPU Processor Count</div>
          <div class="core-count-display">{{ cpuCoreCount }}</div>
        </div>



        <div class="panel-container">
          <div class="panel-title">RootFS Total(GiB)</div>
          <!-- <h2>Rootfs Size (GiB)</h2> -->
          <div class="core-count-display">{{ rootfsSize }} </div>

        </div>

        <div class="panel-container">
          <div class="panel-title">RAM Total(GiB)</div>
          <div class="core-count-display">{{ ramTotal }}</div>
        </div>
      </div>


    </n-card>

    <!-- 2nd Row: Bar Chart -->
    <n-card>
      <div class="panel-row">
        <div class="panel-container">
          <div class="panel-title">CPU Basic </div>
          <div ref="barChartCpu" class="bar-chart"></div>
        </div>
        <div class="panel-container">
          <div class="panel-title">Pressure Over Time</div>
          <div ref="lineChartCpu" class="line-chart"></div>
        </div>

        <!-- <div class="panel-container">
          <div class="panel-title">CPU Cores Count</div> 
          <div class="core-count-display">{{ cpuCoreCount }}</div> 
        </div> -->
      </div>
    </n-card>
    
    <n-card>
      <div class="panel-row">



        <div class="panel-container">
          <div class="panel-title">Network Traffic (Receive/Transmit)</div> <!-- Panel Title -->
          <div ref="networkTrafficChart" class="network-traffic-chart"></div> <!-- Network Traffic Chart -->
        </div>

        <div class="panel-container">
          <div class="panel-title">Uptime (Hours)</div> <!-- Uptime Panel -->
          <div ref="uptimeChart" class="uptime-chart"></div> <!-- Uptime Chart -->
        </div>

      </div>


    </n-card>


    <!-- 4rth row -->





  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts'; // Import ECharts
import { NSelect, NCard } from 'naive-ui';  // Import Naive UI components

const gaugeChartCpu = ref(null);
const gaugeChartSysLoad = ref(null);
const gaugeChartRamLoad = ref(null);
const gaugeChartRootUsed = ref(null);
const barChartCpu = ref(null); // Bar chart ref for 2nd row

// Define state variables
const rootfsSize = ref(null);
const ramTotal = ref(null);
const isLoading = ref(true);
const error = ref(null);

const lineChartCpu = ref(null);
const chartInstanceCpupressure = ref(null);

const cpuPercent = ref(0);
const memPercent = ref(0);
const ioPercent = ref(0);

const uptimeChart = ref(null); // Uptime chart ref

let chartInstanceCpu = null;
let chartInstanceSysLoad = null;
let chartInstanceRamLoad = null;
let chartInstanceRootLoad = null;
let chartInstanceBarCpu = null; // Bar chart instance

let uptimeChartInstance = null; // Uptime chart instance



const selectedJob = ref('');   // Selected Job
const selectedHost = ref('');  // Selected Host
const jobOptions = ref([]);      // Options for Jobs
const hostOptions = ref([]);     // Options for Hosts (All Hosts)
const filteredHostOptions = ref([]); // Filtered Hosts based on Job
const cpuCoreCount = ref(0);     // New ref for CPU core count

const networkTrafficChart = ref(null); // Ref for Network Traffic chart
let chartInstanceNetworkTraffic = null; // Chart instance for Netw

// const selectedHost = ref('ankita-gitlab-ce'); // Use default

// Fetch CPU core count data based on the selected host
const fetchCpuCoreCount = async (host) => {
  try {
    const response = await fetch(`http://172.16.1.119:9090/api/v1/query?query=windows_cs_logical_processors{instance=~"${host}"}`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    if (data.status === 'success') {
      const coreCount = parseInt(data.data.result[0].value[1]); // Extract CPU core count value
      cpuCoreCount.value = coreCount; // Update the CPU core count display
    }
  } catch (error) {
    console.error('Error fetching CPU core count data:', error);
  }
};

// 1st row hard disk usage1 panel Fetch CPU data based on the selected host
const hdUsage = async (host) => {
  try {
    const response = await fetch(`http://172.16.1.119:9090/api/v1/query?query=100 - (windows_logical_disk_free_bytes{instance=~"${host}"} / windows_logical_disk_size_bytes{instance=~"${host}"})*100`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    if (data.status === 'success') {
      const cpuUsage = parseFloat(data.data.result[0].value[1]); // Extract CPU usage value
      updateGauge(chartInstanceCpu, cpuUsage, 'HD Usage'); // Update CPU gauge chart with the fetched value
    }
  } catch (error) {
    console.error('Error fetching CPU data:', error);
  }
};

// Fetch Sys Load data based on the selected host
const fetchSysLoadData = async (host) => {
  try {
    const response = await fetch(`http://172.16.1.119:9090/api/v1/query?query=100 - (avg by (instance) (irate(windows_cpu_time_total{mode="idle", instance=~"${host}"}[1m])) * 100)`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    if (data.status === 'success') {
      const sysLoad = parseFloat(data.data.result[0].value[1]); // Extract Sys Load value
      updateGauge(chartInstanceSysLoad, sysLoad, 'Sys Load'); // Update Sys Load gauge chart with the fetched value
    }
  } catch (error) {
    console.error('Error fetching Sys Load data:', error);
  }
};

// Fetch Ram Load data based on the selected host

const fetchRamData = async (host) => {
  try {
    const response = await fetch(`http://172.16.1.119:9090/api/v1/query?query=(windows_cs_physical_memory_bytes{instance=~"${host}"} - windows_os_physical_memory_free_bytes{instance=~"${host}"}) / windows_cs_physical_memory_bytes{instance=~"${host}"} * 100`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    if (data.status === 'success') {
      const ramLoad = parseFloat(data.data.result[0].value[1]); // Extract Sys Load value
      updateGauge(chartInstanceRamLoad, ramLoad, 'Ram Load'); // Update Sys Load gauge chart with the fetched value
    }
  } catch (error) {
    console.error('Error fetching Ram Load data:', error);
  }
};


// Fetch Root Load data based on the selected host
const fetchRootLoadData = async (host) => {
  try {
    const response = await fetch(`http://172.16.1.119:9090/api/v1/query?query=(sum(windows_logical_disk_size_bytes{volume!~"Harddisk.*", instance="WIN-VF28QPJSC70"}) by (instance) - sum(windows_logical_disk_free_bytes{volume!~"Harddisk.*", instance="WIN-VF28QPJSC70"}) by (instance)) / sum(windows_logical_disk_size_bytes{volume!~"Harddisk.*", instance="WIN-VF28QPJSC70"}) by (instance) * 100`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log(data)

    if (data.status === 'success') {
      const rootLoad = parseFloat(data.data.result[0].value[1]); // Extract Sys Load value
      updateGauge(chartInstanceRootLoad, rootLoad, 'Root fs Used'); // Update Sys Load gauge chart with the fetched value
    }
  } catch (error) {
    console.error('Error fetching Sys Load data:', error);
  }
};

const fetchramTotal = async (host) => {
  try {
    const response = await fetch(`http://172.16.1.119:9090/api/v1/query?query=windows_cs_physical_memory_bytes{instance=~"${host}"}`);

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    const data = await response.json();

    // Check if data exists
    if (data.data && data.data.result.length > 0) {
      // Fetch size in bytes and convert to GiB
      const sizeInBytes = data.data.result[0].value[1];
      ramTotal.value = (sizeInBytes / (1024 ** 3)).toFixed(2); // Convert to GiB
    } else {
      ramTotal.value = 'N/A';
    }
  } catch (err) {
    error.value = `Failed to fetch data: ${err.message}`;
  } finally {
    isLoading.value = false;
  }
};

// Fetch data from API
const fetchRootfsSize = async (host) => {
  try {
    const response = await fetch(`http://172.16.1.119:9090/api/v1/query?query=node_filesystem_size_bytes{instance="${host}",job="integrations/unix",mountpoint="/",fstype!="rootfs"}`);

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    const data = await response.json();

    // Check if data exists
    if (data.data && data.data.result.length > 0) {
      // Fetch size in bytes and convert to GiB
      const sizeInBytes = data.data.result[0].value[1];
      rootfsSize.value = (sizeInBytes / (1024 ** 3)).toFixed(2); // Convert to GiB
    } else {
      rootfsSize.value = 'N/A';
    }
  } catch (err) {
    error.value = `Failed to fetch data: ${err.message}`;
  } finally {
    isLoading.value = false;
  }
};

// Initialize the ECharts instance
const initCpuLineChart = () => {
  if (lineChartCpu.value) {
    chartInstanceCpupressure.value = echarts.init(lineChartCpu.value);
  }
};

// Fetch pressure data (CPU, memory, IO)
// Fetch pressure data (CPU, memory, IO)
const fetchData = async (host) => {
  try {
    const cpuResponse = await fetch(`http://172.16.1.119:9090/api/v1/query?query=irate(node_pressure_cpu_waiting_seconds_total{instance="${host}",job="integrations/unix"}[5m])`);
    const memResponse = await fetch(`http://172.16.1.119:9090/api/v1/query?query=irate(node_pressure_memory_waiting_seconds_total{instance="${host}",job="integrations/unix"}[5m])`);
    const ioResponse = await fetch(`http://172.16.1.119:9090/api/v1/query?query=irate(node_pressure_io_waiting_seconds_total{instance="${host}",job="integrations/unix"}[5m])`);

    // Parse the JSON response
    const cpuData = await cpuResponse.json();
    const memData = await memResponse.json();
    const ioData = await ioResponse.json();

    // Check if the response status is 'success' and update the pressure values
    if (cpuData.status === 'success') {
      cpuPercent.value = parseFloat(cpuData.data.result[0].value[1]);
    }
    if (memData.status === 'success') {
      memPercent.value = parseFloat(memData.data.result[0].value[1]);
    }
    if (ioData.status === 'success') {
      ioPercent.value = parseFloat(ioData.data.result[0].value[1]);
    }

    // Update the line chart with the fetched data
    updateCpuLineChart([
      { type: 'CPU', value: cpuPercent.value },
      { type: 'Memory', value: memPercent.value },
      { type: 'IO', value: ioPercent.value }
    ]);
  } catch (error) {
    console.error('Error fetching pressure data:', error);
  }
};


const updateCpuLineChart = (data) => {
  if (chartInstanceCpupressure.value) {
    const option = {
      title: {
        text: '',
        left: 'center',
        textStyle: {
          color: '#4CAF50',
          fontWeight: 'bold',
          fontSize: 18
        }
      },
      tooltip: {
        trigger: 'axis',
        formatter: '{b}: {c}%'
      },
      xAxis: {
        type: 'category',
        data: data.map(item => item.type),
        axisLabel: {
          rotate: 45,
          color: '#888',
        },
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}%',
          color: '#888',
        },
      },
      series: [
        {
          data: data.map(item => item.value),
          type: 'line',
          smooth: true,
          itemStyle: {
            color: '#4CAF50',
          },
          areaStyle: {
            color: 'rgba(76, 175, 80, 0.2)', // Green area under line
          },
        },
      ],
    };
    chartInstanceCpupressure.value.setOption(option);
  } else {
    console.error('chartInstanceCpupressure is not initialized.');
  }
};



//cpu baic
const fetchCpuBarChartData = async (host) => {
  try {
    const response = await fetch(`http://172.16.1.119:9090/api/v1/query?query=sum(irate(node_cpu_seconds_total{instance="${host}", mode="system"}[5m])) / scalar(count(count(node_cpu_seconds_total{instance="${host}"}) by (cpu)))`);
    const data = await response.json();

    if (data.status === 'success') {
      const cpuUsageData = data.data.result.map((item, index) => {
        const value = parseFloat(item.value[1]).toFixed(2); // Round value to 2 decimal places
        return {
          // CPU label along with the exact value
          cpu: `CPU ${index + 1} (${value}%)`,  // Label will show "CPU 1 (0.45%)"
          value: value,  // The CPU usage value from Prometheus
        };
      });

      console.log(cpuUsageData);
      updateBarChart(chartInstanceBarCpu, cpuUsageData);
    }
  } catch (error) {
    console.error('Error fetching CPU bar chart data:', error);
  }
};

const updateBarChart = (chartInstance, data) => {
  const option = {
    xAxis: {
      type: 'category',
      data: data.map((item) => item.cpu), // Display CPU label with value
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        data: data.map((item) => item.value), // Plot only the value for the bar height
        type: 'bar',
      },
    ],
  };
  chartInstance.setOption(option);
};



// Fetch job and host data for the dropdowns
const fetchJobAndHostData = async () => {
  try {
    const response = await fetch('http://172.16.1.119:9090/api/v1/query?query=windows_logical_disk_free_bytes');

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    if (data.status === 'success') {
      const uniqueJobs = new Set();
      const hosts = [];

      data.data.result.forEach(item => {
        uniqueJobs.add(item.metric.job); // Add Job to Set
        hosts.push({ label: item.metric.instance, value: item.metric.instance, job: item.metric.job }); // Add Host with Job reference
      });

      jobOptions.value = Array.from(uniqueJobs).map(job => ({
        label: job,
        value: job,
      }));

      hostOptions.value = hosts;

      // Set default selected values
      if (jobOptions.value.length > 0) {
        selectedJob.value = jobOptions.value[0].value; // Set the first job as default
      }
      if (hostOptions.value.length > 0) {
        selectedHost.value = hostOptions.value[0].value; // Set the first host as default
      }
    }
  } catch (error) {
    console.error('Error fetching job and host data:', error);
  }
};

// Create Gauge Chart for both CPU and Sys Load
const createGauge = (chartInstance, name) => {
  const option = {
    series: [
      {
        type: 'gauge',
        detail: {
          formatter: '{value}%',   // Show percentage
          fontSize: 20,
          color: '#008000', // green color
        },
        axisLine: {
          lineStyle: {
            color: [
              [0.3, '#67e0e3'],   // Blue for 0-30%
              [0.7, '#37a2da'],   // Light blue for 30-70%
              [1, '#fd666d'],     // Red for 70-100%
            ],
            width: 20,
          },
        },
        pointer: {
          width: 5,              // Pointer width
          length: '60%',
        },
        data: [{ value: 0, name }],
      },
    ],
  };
  chartInstance.setOption(option);
};

// Update Gauge Chart with the new value
const updateGauge = (chartInstance, value, name) => {
  chartInstance.setOption({
    series: [
      {
        data: [{ value: value.toFixed(2), name }],
      },
    ],
  });
};


// Initialize the ECharts instance for Uptime
const initUptimeChart = () => {
  if (uptimeChart.value) {
    uptimeChartInstance = echarts.init(uptimeChart.value);
  }
};

// Function to update Uptime chart
const updateUptimeChart = (uptimeData) => {
  if (uptimeChartInstance) {
    const option = {
      title: {
        text: '',
        left: 'center',
        textStyle: {
          color: '#4CAF50',
          fontWeight: 'bold',
          fontSize: 18
        }
      },
      xAxis: {
        type: 'category',
        data: ['Uptime'],
        axisLabel: {
          rotate: 45,
          color: '#888',
        },
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value} hours',
          color: '#888',
        },
      },
      series: [
        {
          data: [uptimeData],
          type: 'bar',
          itemStyle: {
            color: '#bce3be',
          },
        },
      ],
    };
    uptimeChartInstance.setOption(option);
  }
};

// Fetch Uptime data based on the selected host
const fetchUptimeData = async (host) => {
  try {
    const response = await fetch(
      `http://172.16.1.119:9090/api/v1/query?query=node_time_seconds{instance="${host}"} - node_boot_time_seconds{instance="${host}"}`
    );

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    if (data.status === 'success') {
      const uptimeSeconds = parseFloat(data.data.result[0].value[1]);
      const uptimeHours = (uptimeSeconds / 3600).toFixed(2); // Convert uptime to hours
      updateUptimeChart(uptimeHours); // Update the chart with uptime
    }
  } catch (error) {
    console.error('Error fetching Uptime data:', error);
  }
};

const fetchNetworkTrafficData = async (host) => {
  try {
    // Fetch receive and transmit traffic data
    const receiveResponse = await fetch(`http://172.16.1.119:9090/api/v1/query?query=irate(node_network_receive_bytes_total{instance="${host}"}[5m])*8`);
    const transmitResponse = await fetch(`http://172.16.1.119:9090/api/v1/query?query=irate(node_network_transmit_bytes_total{instance="${host}"}[5m])*8`);

    const receiveData = await receiveResponse.json();
    const transmitData = await transmitResponse.json();

    console.log('Receive Data:', receiveData);
    console.log('Transmit Data:', transmitData);

    // Check if both queries were successful
    if (receiveData.status === 'success' && transmitData.status === 'success') {
      const receiveResult = receiveData.data.result || [];
      const transmitResult = transmitData.data.result || [];

      let receiveValues = [];
      let transmitValues = [];

      // Check if receive result has valid data
      if (receiveResult.length > 0 && receiveResult[0].value) {
        const [time, value] = receiveResult[0].value;
        receiveValues.push([time * 1000, parseFloat(value)]); // Convert time to ms and value to float
      } else {
        console.error("Receive Data does not have valid 'value' array");
      }

      // Check if transmit result has valid data
      if (transmitResult.length > 0 && transmitResult[0].value) {
        const [time, value] = transmitResult[0].value;
        transmitValues.push([time * 1000, parseFloat(value)]); // Convert time to ms and value to float
      } else {
        console.error("Transmit Data does not have valid 'value' array");
      }

      // Update the chart only if valid data was fetched
      if (receiveValues.length > 0 && transmitValues.length > 0) {
        updateNetworkTrafficChart(chartInstanceNetworkTraffic, receiveValues, transmitValues); // Update chart
      } else {
        console.error("No valid data to update the chart.");
      }
    } else {
      console.error("Error in fetching data from Prometheus. Status not success.");
    }
  } catch (error) {
    console.error('Error fetching Network Traffic data:', error);
  }
};

// Function to update the chart
const updateNetworkTrafficChart = (chartInstance, receiveData, transmitData) => {
  const option = {
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: ['Receive Traffic', 'Transmit Traffic'],
    },
    xAxis: {
      type: 'time',
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: (value) => `${(value / 1024 / 1024).toFixed(2)} Mbps`, // Convert to Mbps
      },
    },
    series: [
      {
        name: 'Receive Traffic',
        type: 'line',
        data: receiveData,
        areaStyle: {}, // Area chart for receive traffic
        smooth: true, // Smooth lines
      },
      {
        name: 'Transmit Traffic',
        type: 'line',
        data: transmitData,
        smooth: true, // Smooth lines
        lineStyle: {
          type: 'dashed', // Dashed line for transmit traffic
        },
      },
    ],
  };
  chartInstance.setOption(option);
};




// Filter hosts based on the selected job
const onJobSelect = (job) => {
  filteredHostOptions.value = hostOptions.value.filter(host => host.job === job); // Filter hosts by selected job
  selectedHost.value = null; // Reset selected host when job changes
};

// Fetch data for both CPU and Sys Load when a host is selected
const onHostSelect = (host) => {
  hdUsage(host);
  fetchSysLoadData(host);
  fetchRamData(host);
  fetchRootLoadData(host);
  fetchCpuBarChartData(host);
  fetchCpuCoreCount(host); // Fetch CPU core count when host is selected
  fetchData(host);
  fetchUptimeData(host); // Fetch uptime data for default host (example)
  fetchRootfsSize(host);
  fetchramTotal(host);
  fetchNetworkTrafficData(host);



};
onMounted(() => {
  chartInstanceCpu = echarts.init(gaugeChartCpu.value);   // Initialize CPU gauge chart
  chartInstanceSysLoad = echarts.init(gaugeChartSysLoad.value); // Initialize Sys Load gauge chart
  chartInstanceRamLoad = echarts.init(gaugeChartRamLoad.value); // Initialize Sys Load gauge chart
  chartInstanceRootLoad = echarts.init(gaugeChartRootUsed.value); // Initialize Sys Load gauge chart
  chartInstanceBarCpu = echarts.init(barChartCpu.value); // Initialize bar

  chartInstanceNetworkTraffic = echarts.init(networkTrafficChart.value); // Initialize chart on mount
  fetchNetworkTrafficData(); // Fetch initial data

  createGauge(chartInstanceCpu, '');             // Create the initial CPU gauge chart
  createGauge(chartInstanceSysLoad, '');          // Create the initial Sys Load gauge chart
  createGauge(chartInstanceRamLoad, '');          // Create the initial Sys Load gauge chart

  createGauge(chartInstanceRootLoad, '');          // Create the initial Sys Load gauge chart
  fetchRootfsSize();
  fetchramTotal();




  fetchJobAndHostData();
  initCpuLineChart();
  fetchData();
  initUptimeChart(); // Initialize Uptime chart
  fetchUptimeData(); // Fetch uptime data for default host (example)

});


</script>

<style scoped>
/* Dropdown container styling */
.dropdown-container {
  display: flex;
  margin-bottom: 20px;
  gap: 20px;
}

.time-series-chart {
  width: 100%;
  height: 300px;
  margin: 0 auto;
}

/* Individual dropdown-item */
.dropdown-item {
  display: flex;
  align-items: center;
}

/* Label box styling */
.label-box {
  width: 50px;
  text-align: right;
  margin-right: 10px;
  padding: 5px;
  font-weight: bold;
}

.bar-chart {
  width: 100%;
  height: 300px;
  margin: 0 auto;
}

.core-count-display {
  font-size: 50px;
  color: #0c6e14;
  /* Green color for text */
  text-align: center;
  margin-top: 30px;
  font-weight: bold;
  background-color: #eff0f5;
  /* Green background for square */
  height: 220px;
  /* Equal height */
  width: 220px;
  /* Equal width */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  /* Optional: Add border-radius for smooth edges */
  margin-left: 180px;
}

.rootfs-display {
  font-size: 35px;
  color: #0c6e14;
  /* Green color for text */
  text-align: center;
  margin-top: 30px;
  font-weight: bold;
  background-color: #eff0f5;
  /* Green background for square */
  height: 220px;
  /* Equal height */
  width: 220px;
  /* Equal width */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  /* Optional: Add border-radius for smooth edges */
  margin-left: 50px;
}



/* Chart container */
.chart-container {
  width: 400px;
  height: 300px;
}

/* Panel row layout */
.panel-row {
  display: flex;
  /* justify-content: space-between; */
  /* gap: 20px; */
}

/* Panel container */
.panel-container {
  flex: 1;
  /* Allow panels to be of equal size */
  min-width: 250px;
  /* Set a minimum width so panels are not too small */
  height: 300px;
  /* Set height for the charts */
  text-align: center;
}

.line-chart {
  width: 100%;
  height: 300px;
  margin-top: 0.1em;
}

.pressure-values {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin-bottom: 10px;
}

.gauge-chart {
  width: 100%;
  height: 100%;
  /* margin-bottom: 10px; */
  ;
}

/* Row layout for the charts */
.chart-row {
  display: flex;
  justify-content: space-between;
  /* gap: 20px; */
}

.panel-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

/* Add any custom styles for the uptime chart if needed */
.uptime-chart {
  width: 100%;
  height: 300px;
  margin-right: 100px;
}

.network-traffic-chart {
  width: 100%;
  height: 300px;
}
</style>
