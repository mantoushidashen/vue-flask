<template>
  <div
    class="novel-reader"
    ref="novelReader"
    :style="{
      backgroundColor: selectedBackground,
      fontFamily: selectedFontFamily,
      fontSize: selectedFontSize + 'px',
    }"
  >
    <!-- 显示当前章节内容 -->
    <el-card class="chapter-content" shadow="never">
      <div
        v-for="(paragraph, index) in currentChapterContent"
        :key="index"
        class="paragraph"
      >
        {{ paragraph }}
      </div>
    </el-card>

    <!-- 控制按钮和章节信息 -->
    <div class="controls">
      <el-row type="flex" justify="center" align="middle">
        <el-col :xs="{ span: 24 }" :sm="{ span: 12 }">
          <div class="chapter-info">{{ title }} / {{ totalChapters }} 章</div>
        </el-col>
        <el-col :xs="{ span: 24 }" :sm="{ span: 12 }">
          <el-button-group>
            <el-button
              type="primary"
              @click="previousPageFlag ? previousPage() : previousChapter()"
              :disabled="chapterIndex === 0 && !previousPageFlag"
            >
              <template v-if="previousPageFlag"
                >上一页<i class="el-icon-arrow-right el-icon--right"></i
              ></template>
              <template v-else
                >上一章<i class="el-icon-arrow-right el-icon--right"></i
              ></template>
            </el-button>

            <el-button
              type="primary"
              @click="nextPageFlag ? nextPage() : nextChapter()"
              :disabled="chapterIndex === chapters.length - 1"
            >
              <template v-if="nextPageFlag"
                >下一页<i class="el-icon-arrow-right el-icon--right"></i
              ></template>
              <template v-else
                >下一章<i class="el-icon-arrow-right el-icon--right"></i
              ></template>
            </el-button>
          </el-button-group>
        </el-col>
      </el-row>
    </div>

    <!-- 背景选择工具条 -->
    <div class="background-selector">
      <div class="setting-label"></div>
      <div
        class="theme-option"
        v-for="(bg, index) in backgroundOptions"
        :key="index"
        @click="changeBackground(bg.color)"
        :style="{ backgroundColor: bg.color }"
      ></div>
    </div>

    <!-- 字体设置工具条 -->
    <div class="font-selector">
      <div class="setting-label">字体设置</div>
      <el-select v-model="selectedFontFamily" placeholder="选择字体">
        <el-option
          v-for="font in fontOptions"
          :key="font.value"
          :label="font.label"
          :value="font.value"
        />
      </el-select>
      <el-select v-model="selectedFontSize" placeholder="选择字号">
        <el-option
          v-for="size in fontSizeOptions"
          :key="size"
          :label="size + 'px'"
          :value="size"
        />
      </el-select>
    </div>
  </div>
</template>
  

<script>
import { getNovelChapters, getNovelChapterContent } from "@/api/novel";

export default {
  name: "Story",
  data() {
    return {
      chapters: [],
      chapterIndex: 0, // 当前章节索引
      currentChapterContent: [], // 当前章节内容
      title: "",
      nextPageFlag: false,
      previousPageFlag: true,
      chapterUrl: "",
      nextPageUrl: "",
      pageList: [],
      pageIndex: 0,
      scrollPosition: 0, // 储存滚动位置
      selectedBackground: "#FFFFFF",
      selectedFontFamily: '"Times New Roman", Times, serif',
      selectedFontSize: 20,
      backgroundOptions: [
        { color: "#FFFFFF" },
        { color: "#F8DE7E" },
        { color: "#FFF2E2" },
        { color: "#F5F5DC" },
        // ...其他背景颜色...
      ],
      fontOptions: [
        { label: "Times New Roman", value: '"Times New Roman", Times, serif' },
        { label: "Arial", value: "Arial, sans-serif" },
        { label: "Georgia", value: "Georgia, serif" },
        // ...其他字体选项...
      ],
      fontSizeOptions: [16, 18, 20, 22, 24], // 字号选项
    };
  },
  computed: {
    totalChapters() {
      return this.chapters.length;
    },
  },
  methods: {
    async fetchChapters() {
      try {
        const response = await getNovelChapters();
        this.chapters = response.data;
        this.chapterUrl = this.chapters[0].url;
        this.fetchChapterContent(this.chapterUrl);
      } catch (error) {
        console.error("Error fetching chapters:", error);
      }
    },
    async fetchChapterContent(chapterUrl) {
      if (this.chapterIndex < 0 || this.chapterIndex >= this.totalChapters) {
        return;
      }
      try {
        this.title = this.chapters[this.chapterIndex].title;
        const response = await getNovelChapterContent(chapterUrl);
        this.pageList.push(response.data.url);
        this.currentChapterContent = response.data.content.split("\n");

        if (response.data.next_page != null) {
          this.nextPageFlag = true;
          this.nextPageUrl = response.data.next_page;
        } else {
          this.nextPageFlag = false;
        }
      } catch (error) {
        console.error("Error fetching chapter content:", error);
      }
    },
    nextPage() {
      if (this.chapterIndex <= this.totalChapters - 1) {
        this.fetchChapterContent(this.nextPageUrl);
        this.pageIndex += 1;
        this.previousPageFlag = true;
      }
    },
    previousPage() {
      if (this.chapterIndex >= 0) {
        this.pageIndex -= 1;
        if (this.pageIndex == 0) {
          this.previousPageFlag = false;
        }
        this.fetchChapterContent(this.pageList[this.pageIndex]);
      }
    },
    previousChapter() {
      if (this.chapterIndex > 0) {
        this.pageIndex = 0;
        this.previousPageFlag = false;
        this.nextPageFlag = true;
        this.chapterIndex--;
        this.fetchChapterContent(this.chapters[this.chapterIndex].url);
      }
    },
    nextChapter() {
      if (this.chapterIndex < this.totalChapters - 1) {
        this.pageIndex = 0;
        this.chapterIndex++;
        this.previousPageFlag = false;
        this.nextPageFlag = true;
        this.fetchChapterContent(this.chapters[this.chapterIndex].url);
      }
    },
    saveScrollPosition() {
      if (this.$refs.novelReader) {
        this.scrollPosition = this.$refs.novelReader.scrollTop;
        console.log(this.scrollPosition);
      }
    },
    restoreScrollPosition() {
      if (this.$refs.novelReader) {
        this.$refs.novelReader.scrollTop = this.scrollPosition;
      }
    },
    changeBackground(color) {
      this.selectedBackground = color;
    },
  },
  created() {
    // 当组件创建后立即获取章节列表
    this.fetchChapters();
  },
  mounted() {
    this.$refs.novelReader.addEventListener("scroll", this.saveScrollPosition);
    console.log(this.$refs.novelReader.scrollTop);
  },
  beforeDestroy() {
    this.$refs.novelReader.removeEventListener(
      "scroll",
      this.saveScrollPosition
    );
  },
  activated() {
    this.$nextTick(() => {
      this.restoreScrollPosition();
    });
  },
  deactivated() {
    this.saveScrollPosition();
  },
};
</script>

<style scoped>
/* 样式部分 */
.novel-reader {
  max-width: 1200px; /* 限制最大宽度 */
  margin: 0 auto; /* 水平居中 */
  padding: 20px; /* 添加一些内边距 */
  overflow-y: auto;
  /* 添加过渡效果 */
  transition: background-color 0.3s;
}

/* 背景选择工具条 */
.background-selector {
  position: fixed;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.9);
  padding: 10px;
  border-radius: 8px 0 0 8px;
}

/* 字体设置工具条 */
.font-selector {
  position: fixed;
  right: 2%; /* 将字体选择器放在屏幕中间 */
  transform: translateX(-50%) translateY(-50%); /* 使用transform属性进行微调 */
  top: 50%;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  background: inherit;
  padding: 10px;
  border-radius: 0 8px 8px 0;
  /* 添加最大宽度防止元素太宽 */
  max-width: 500px; /* 根据需要调整 */
}

.setting-label {
  font-family: 'Times New Roman', Times, serif;
  font-size: 16px; /* 增加字体大小 */
  color: #4a4a4a; /* 深灰色的字体颜色 */
  font-weight: bold; /* 加粗文字 */
  text-align: left; /* 文字左对齐 */
  margin: 10px 0; /* 上下间距 */
  padding-left: 10px; /* 左侧填充，如果需要 */
}

/* 如果需要对移动设备做特别调整 */
@media (max-width: 768px) {
  .setting-label {
    /* 移动设备上的样式调整 */
    font-size: 14px; /* 移动设备上可能需要更小的字体大小 */
  }
}

.theme-option {
  width: 40px;
  height: 40px;
  margin-bottom: 10px;
  cursor: pointer;
  border: 1px solid #ebebeb;
}

/* Element UI select样式调整 */
.el-select {
  margin-bottom: 10px;
}

/* 确保 .chapter-content 根据设置的样式生效 */
.chapter-content {
  min-height: 70vh;
  margin-bottom: 20px;
  padding: 30px;
  font-family: inherit; /* 继承 .novel-reader 的字体 */
  font-size: inherit; /* 继承 .novel-reader 的字号 */
  line-height: 1.6;
  color: #020202;
  background-color: inherit;
}

/* 适配不同屏幕尺寸 */
@media (max-width: 768px) {
  .background-selector,
  .font-selector {
    top: initial;
    bottom: 10px; /* 调整为底部出现 */
    transform: none; /* 移除转换效果 */
    left: 10px; /* 在小屏幕上将其显示在左侧 */
    right: auto; /* 重置右侧偏移 */
    flex-direction: row; /* 横向排列 */
  }
  .theme-option {
    width: 24px; /* 调整大小以适应屏幕 */
    height: 24px;
  }
  .font-selector {
    left: 10px; /* 防止选择器贴近屏幕边缘 */
    right: 10px; /* 添加右侧间距 */
    margin-left: 0; /* 重置左边距 */
  }
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