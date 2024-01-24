<template>
  <div class="mixin-components-container">
    <el-row>
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>Excel文件对比分析</span>
        </div>
        <div style="margin-bottom: 50px">
          <el-upload
            class="upload-demo"
            action="/api/upload"
            :on-change="beforeUpload"
            :file-list="fileList"
            :auto-upload="false"
            :limit="2"
            accept=".xlsx"
          >
            <el-button slot="trigger" size="small" type="primary" :plain="true"
              >选取文件</el-button
            >
            <el-button
              style="margin-left: 10px"
              size="small"
              type="success"
              @click="submitUpload"
              >开始分析</el-button
            >
            <el-button @click="getExcelFile" size="small" type="primary" icon="el-icon-download">下载</el-button>
          </el-upload>
        </div>
      </el-card>
    </el-row>

    <el-row :gutter="20" style="margin-top:50px;">
      <el-col :span="12">
        <el-card class="box-card">
          <div id="demandGraph" :style="{width: '800px', height: '300px'}"></div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="box-card">
          <div id="shinryGraph" :style="{width: '800px', height: '300px'}"></div>
        </el-card>
      </el-col>

      <!-- 客户意见状态 -->
      <el-col :span="8" style="margin-top:10px;">
        <el-card class="box-card">
          <div id="crsOpinionGraph" :style="{width: '500px', height: '300px'}"></div>
        </el-card>
      </el-col>
      <!-- 客户需求状态 -->
      <el-col :span="8" style="margin-top:10px;">
        <el-card class="box-card">
          <div id="crsDemandGraph" :style="{width: '500px', height: '300px'}"></div>
        </el-card>
      </el-col>
      
      <!-- 客户需求 -->
      <el-col :span="8" style="margin-top:10px;">
        <el-card class="box-card">
          <div id="crsGraph" :style="{width: '500px', height: '300px'}"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 系统需求情况 -->
    <el-row :gutter="20" style="margin-top:50px;">
      <el-col :span="8">
        <el-card class="box-card">
          <div id="shinryGraph" :style="{width: '800px', height: '300px'}"></div>
        </el-card>
      </el-col>

      <!-- 系统需求状态 -->
      <el-col :span="8">
        <el-card class="box-card">
          <div id="systemStatusGraph" :style="{width: '600px', height: '300px'}"></div>
        </el-card>
      </el-col>
      
      <!-- 系统需求向上追溯 -->
      <el-col :span="8">
        <el-card class="box-card">
          <div id="sysrsGraph" :style="{width: '600px', height: '300px'}"></div>
        </el-card>
      </el-col>


    </el-row>

  </div>
</template>

<script>

import { uploadFile, getFile } from '@/api/upload'
export default {
name: "upload",
  data() {
    return {
      date: undefined,
      fileList: [],
      crs_total: '',
      crs_s_num: '',
      crs_sh_num: '',
      crs_h_num: '',
      crs_hm_num: '',
      crs_m_num: '',
      crs_shm_num: '',

      shinry_access: '',
      shinry_not_access: '',
      shinry_condition_access: '',

      crs_access: '',
      crs_not_access: '',
      crs_condition_access: '',

      crs_draft: '',
      crs_review: '',
      crs_approve: '',
      crs_obsolete: '',

      sysrs_draft: '',
      sysrs_review: '',
      sysrs_approve: '',
      sysrs_obsolete: '',

    };
  },
  mounted(){
    this.drawLine();
    this.shinryLine();
    this.opinionLine();
    this.demandyLine();
    this.crsLine();
    this.sysrsDemandyLine();
    this.sysrsLine();
  },
  methods: {
    submitUpload() {
      if (this.fileList.length == 2) {
        // 获取当前时间戳，将时间戳返回给后端用于当作文件名称
        const dateTime = new Date().getTime()
        this.date = dateTime

        const formData = new FormData()
        formData.append('date', dateTime)
        this.fileList.forEach(file => {
          formData.append('file', file.raw)
        })
        // 请求后台接口数据
        uploadFile(formData).then(res=> {
          this.$nextTick( ()=>{
            if (res.code == 20000) {
              this.crs_total = res.data.crs_total
              this.crs_s_num = res.data.crs_s_num
              this.crs_sh_num = res.data.crs_sh_num
              this.crs_h_num = res.data.crs_h_num
              this.crs_hm_num = res.data.crs_hm_num
              this.crs_m_num = res.data.crs_m_num
              this.crs_shm_num = res.data.crs_shm_num
              this.drawLine(this.crs_total, this.crs_s_num , this.crs_sh_num, this.crs_h_num,this.crs_hm_num, this.crs_m_num, this.crs_shm_num)

              this.shinry_access = res.data.shinry_access
              this.shinry_not_access = res.data.shinry_not_access
              this.shinry_condition_access = res.data.shinry_condition_access
              this.shinryLine(this.shinry_access, this.shinry_not_access, this.shinry_condition_access)

              this.crs_access = res.data.crs_access
              this.crs_not_access = res.data.crs_not_access
              this.crs_condition_access = res.data.crs_condition_access
              this.opinionLine(this.crs_access, this.crs_not_access, this.crs_condition_access)

              this.crs_draft = res.data.crs_draft
              this.crs_review = res.data.crs_review
              this.crs_approve = res.data.crs_approve
              this.crs_obsolete = res.data.crs_obsolete
              this.demandyLine(this.crs_draft, this.crs_review, this.crs_approve, this.crs_obsolete)

              this.sysrs_draft = res.data.sysrs_draft
              this.sysrs_review = res.data.sysrs_review
              this.sysrs_approve = res.data.sysrs_approve
              this.sysrs_obsolete = res.data.sysrs_obsolete
              this.sysrsDemandyLine(this.sysrs_draft, this.sysrs_review, this.sysrs_approve, this.sysrs_obsolete)
            }else{
              this.$message({
                message: res.msg,
                type: "warning"
              })
            }

          })

        })
      }else if (this.fileList.length < 2) {
        console.log(this.fileList)
        this.$message({
          message: "需要两个两件才能进行分析，分别为系统需求文件以及客户需求文件",
          type: 'warning'
        })
      }
    },  
    beforeUpload(file, fileList){
        // 1、判断文件名是否重复，不允许上传相同文件
        let existFile = fileList.slice(0, fileList.length - 1).find(f => f.name === file.name)
        if(existFile){
          fileList.pop()
          this.$message({
            message: file.name+" 文件已存在！",
            type: 'warning'
          })
        }
        this.fileList = fileList;
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    },
    getExcelFile() {
       window.open(
        '/download/' + this.date + '.xlsx',
        '_self'
       )
    },
    // 客户需求分配 
    drawLine(){
        // 基于刚刚准备好的 DOM 容器，初始化 EChart 实例
        let demandGraph = this.$echarts.init(document.getElementById('demandGraph'))
        // 绘制图表
        demandGraph.resize({
          width: 800,
          hright: 300
        })
        demandGraph.setOption({
            title:{
              text: "客户需求分配情况",
              subtext: "需求总数为:" + this.crs_total,
              left: '40%'
            },
            tooltip: {
              trigger: 'item'
            },
            legend: {
              orient: 'vertical',
              left: 'left'
            },
            series: [
              {
                type: 'pie',
                radius: '50%',
                center: ['55%', '60%'],
                data: [
                  { value: this.crs_s_num, name: '软件' },
                  { value: this.crs_h_num, name: '硬件' },
                  { value: this.crs_m_num, name: '结构' },
                  { value: this.crs_sh_num, name: '软件/硬件' },
                  { value: this.crs_hm_num, name: '硬件/结构' },
                  { value: this.crs_shm_num, name: '软件/硬件/结构' }
                ],
                label: {
                  formatter:function(data) {
                    return `${data.name}  ${data.value}\n(${data.percent.toFixed(1)}%)`
                  }
                },

              }
            ]
        });
    },
    // 软件部意见状态
    shinryLine(){
        // 基于刚刚准备好的 DOM 容器，初始化 EChart 实例
        let shinryGraph = this.$echarts.init(document.getElementById('shinryGraph'))
        // 绘制图表
        shinryGraph.resize({
          width: 800,
          hright: 300
        })
        shinryGraph.setOption({
            title:{
              text: "软件部意见接受状态",
              left: '30%'
            },
            tooltip: {
              trigger: 'item'
            },
            legend: {
              orient: 'vertical',
              left: 'left'
            },
            series: [
              {
                type: 'pie',
                radius: '50%',
                center: ['55%', '60%'],
                data: [
                  { value: this.shinry_access, name: '接受' },
                  { value: this.shinry_not_access, name: '不接受' },
                  { value: this.shinry_condition_access, name: '有条件接受' }
                ],
                label: {
                  formatter:function(data) {
                    return `${data.name}  ${data.value}\n(${data.percent.toFixed(1)}%)`
                  }
                },

              }
            ]
        });
    },
    // 客户意见状态
    opinionLine(){
        // 基于刚刚准备好的 DOM 容器，初始化 EChart 实例
        let crsOpinionGraph = this.$echarts.init(document.getElementById('crsOpinionGraph'))
        // 绘制图表
        crsOpinionGraph.resize({
          width: 500,
          hright: 300
        })
        crsOpinionGraph.setOption({
            title:{
              text: "客户意见状态",
              left: '40%'
            },
            tooltip: {
              trigger: 'item'
            },
            legend: {
              orient: 'vertical',
              left: 'left'
            },
            series: [
              {
                type: 'pie',
                radius: '50%',
                center: ['60%', '60%'],
                data: [
                  { value: this.crs_access, name: '客户接受' },
                  { value: this.crs_not_access, name: '客户不接受' },
                  { value: this.crs_condition_access, name: '客户有条件接受' }
                ],
                label: {
                  formatter:function(data) {
                    return `${data.name}  ${data.value}\n(${data.percent.toFixed(1)}%)`
                  }
                },

              }
            ]
        });
    },
    // 客户需求状态
    demandyLine(){
        // 基于刚刚准备好的 DOM 容器，初始化 EChart 实例
        let crsDemandGraph = this.$echarts.init(document.getElementById('crsDemandGraph'))
        // 绘制图表
        crsDemandGraph.resize({
          width: 500,
          hright: 300
        })
        crsDemandGraph.setOption({
            title:{
              text: "客户需求状态",
              left: '40%'
            },
            tooltip: {
              trigger: 'item'
            },
            legend: {
              orient: 'vertical',
              left: 'left'
            },
            series: [
              {
                type: 'pie',
                radius: '50%',
                center: ['60%', '60%'],
                data: [ 
                  { value: this.crs_approve, name: '已批准' },
                  { value: this.crs_review, name: '评审中' },
                  { value: this.crs_draft, name: '草稿' },
                  { value: this.crs_obsolete, name: '已失效' }
                ],
                label: {
                  formatter:function(data) {
                    return `${data.name}  ${data.value}\n(${data.percent.toFixed(1)}%)`
                  }
                },

              }
            ]
        });
    },
    // 客户需求向下覆盖情况
    crsLine(){
        // 基于刚刚准备好的 DOM 容器，初始化 EChart 实例
        let crsGraph = this.$echarts.init(document.getElementById('crsGraph'))
        // 绘制图表
        crsGraph.resize({
          width: 500,
          hright: 300
        })
        crsGraph.setOption({
            title:{
              text: "客户需求向下覆盖情况",
              left: '40%'
            },
            tooltip: {
              trigger: 'item'
            },
            legend: {
              orient: 'vertical',
              left: 'left'
            },
            series: [
              {
                type: 'pie',
                radius: '50%',
                center: ['60%', '60%'],
                data: [
                  { value: 50, name: '向下覆盖' },
                  { value: 10, name: '未向下覆盖' },
                ],
                label: {
                  formatter:function(data) {
                    return `${data.name}  ${data.value}\n(${data.percent.toFixed(1)}%)`
                  }
                },

              }
            ]
        });
    },
    // 系统需求状态
    sysrsDemandyLine(){
        // 基于刚刚准备好的 DOM 容器，初始化 EChart 实例
        let systemStatusGraph = this.$echarts.init(document.getElementById('systemStatusGraph'))
        // 绘制图表
        systemStatusGraph.resize({
          width: 500,
          hright: 300
        })
        systemStatusGraph.setOption({
            title:{
              text: "系统需求状态",
              left: '40%'
            },
            tooltip: {
              trigger: 'item'
            },
            legend: {
              orient: 'vertical',
              left: 'left'
            },
            series: [
              {
                type: 'pie',
                radius: '50%',
                center: ['60%', '60%'],
                data: [ 
                  { value: this.sysrs_approve, name: '已批准' },
                  { value: this.sysrs_review, name: '评审中' },
                  { value: this.sysrs_draft, name: '草稿' },
                  { value: this.sysrs_obsolete, name: '已失效' }
                ],
                label: {
                  formatter:function(data) {
                    return `${data.name}  ${data.value}\n(${data.percent.toFixed(1)}%)`
                  }
                },

              }
            ]
        });
    },
    // 系统需求向上覆盖情况
    sysrsLine(){
        // 基于刚刚准备好的 DOM 容器，初始化 EChart 实例
        let sysrsGraph = this.$echarts.init(document.getElementById('sysrsGraph'))
        // 绘制图表
        sysrsGraph.resize({
          width: 500,
          hright: 300
        })
        sysrsGraph.setOption({
            title:{
              text: "系统需求向上覆盖情况",
              left: '40%'
            },
            tooltip: {
              trigger: 'item'
            },
            legend: {
              orient: 'vertical',
              left: 'left'
            },
            series: [
              {
                type: 'pie',
                radius: '50%',
                center: ['60%', '60%'],
                data: [
                  { value: 50, name: '向上覆盖' },
                  { value: 10, name: '未向上覆盖' },
                ],
                label: {
                  formatter:function(data) {
                    return `${data.name}  ${data.value}\n(${data.percent.toFixed(1)}%)`
                  }
                },

              }
            ]
        });
    },
  },
};
</script>
  
<style scoped>
.mixin-components-container {
  background-color: #f0f2f5;
  padding: 30px;
  min-height: calc(100vh - 84px);
}
.component-item {
  min-height: 100px;
}
</style>