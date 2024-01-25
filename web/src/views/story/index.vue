<template>
  <div class="novel-reader">
    <!-- 显示当前章节内容 -->
    <el-card class="chapter-content" shadow="never">
      <el-scrollbar wrap-class="scrollbar-wrapper">
        <!-- <a>{{ chapters }}</a> -->
        <div
          v-for="(paragraph, index) in currentChapterContent"
          :key="index"
          class="paragraph"
        >
          {{ paragraph }}
        </div>
      </el-scrollbar>
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
  </div>
</template>
  

  <script>
import { getNovelChapters, getNovelChapterContent } from "@/api/novel";

export default {
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
        console.log(response);
        this.chapters = response.data;
        // 在获取到章节列表后，加载第一章的内容
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
  },
  created() {
    // 当组件创建后立即获取章节列表
    this.fetchChapters();
  },
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
  font-family: "Times New Roman", Times, serif; /* 设置字体 */
  font-size: 20px;
  line-height: 1.6;
  background-color: #eceaea; /* 轻微的背景颜色 */
  color: #020202;
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