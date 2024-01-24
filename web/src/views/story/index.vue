<template>
    <div class="novel-reader">
      <!-- 显示当前章节内容 -->
      <el-card class="chapter-content" shadow="never">
        <el-scrollbar wrap-class="scrollbar-wrapper">
          <div v-for="(paragraph, index) in currentChapter" :key="index" class="paragraph">
            {{ paragraph }}
          </div>
        </el-scrollbar>
      </el-card>
  
      <!-- 控制按钮和章节信息 -->
      <div class="controls">
        <el-row type="flex" justify="center" align="middle">
          <el-col :xs="{ span: 24 }" :sm="{ span: 12 }">
            <div class="chapter-info">
              第 {{ chapterIndex + 1 }} 章 / {{ totalChapters }} 章
            </div>
          </el-col>
          <el-col :xs="{ span: 24 }" :sm="{ span: 12 }">
            <el-button-group>
              <el-button type="primary" icon="el-icon-arrow-left" @click="previousChapter" :disabled="chapterIndex === 0">上一章</el-button>
              <el-button type="primary" @click="nextChapter" :disabled="chapterIndex === totalChapters - 1">下一章<i class="el-icon-arrow-right el-icon--right"></i></el-button>
            </el-button-group>
          </el-col>
        </el-row>
      </div>
    </div>
  </template>
  
   
  <script>
  export default {
    data() {
      return {
        chapters: [ // 所有章节内容数组
          ["这里是第一章的文字"],
          ["这里是第二章的文字"],
          ["这里是第三章的文字"]
        ],
        chapterIndex: 0 // 当前章节索引
      };
    },
    
    computed: {
      currentChapter() {
        if (this.chapterIndex >= this.chapters.length || this.chapterIndex < 0) {
          return [];
        } else {
          return this.chapters[this.chapterIndex];
        }
      },
      
      totalChapters() {
        return this.chapters.length;
      }
    },
    
    methods: {
      previousChapter() {
        if (this.chapterIndex > 0) {
          this.chapterIndex--;
        }
      },
      
      nextChapter() {
        if (this.chapterIndex < this.totalChapters - 1) {
          this.chapterIndex++;
        }
      }
    }
  };
  </script>
   
<style scoped>
   /* 样式部分 */
   .novel-reader {
     max-width: 1200px; /* 限制最大宽度 */
     margin: 0 auto; /* 水平居中 */
     padding: 20px; /* 添加一些内边距 */
   }
   
   .chapter-content {
     min-height: 70vh; /* 设置最小高度 */
     margin-bottom: 20px;
     padding: 30px; /* 内部间距 */
     font-family: 'Times New Roman', Times, serif; /* 设置字体 */
     font-size: 18px;
     line-height: 1.6;
     background-color: #f9f9f9; /* 轻微的背景颜色 */
   }
   
   .paragraph {
     text-indent: 2em;
     margin-bottom: 10px;
   }
   
   .scrollbar-wrapper {
     height: 100%; /* 滚动条容器高度 */
   }
   
   .controls .chapter-info {
     text-align: center;
     font-size: 1.1em;
     margin-bottom: 10px;
   }
   
   .controls .el-button-group {
     display: flex;
     justify-content: center;
   }
   
   .controls .el-button {
     margin: 0 5px; /* 按钮之间的间隔 */
   }
   
   /* 适配不同屏幕尺寸 */
   @media (max-width: 768px) {
     .novel-reader {
       padding: 10px;
     }
     .chapter-content {
       padding: 15px;
       font-size: 16px;
     }
   }
</style>