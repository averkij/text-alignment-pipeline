<template>
  <div>
    <div class="d-flex">
      <div class="text-h3 mt-5 align-self-start">🤗</div>
      <div class="text-h3 mt-5 pl-3">
        Hello, <span class="text-capitalize">{{ username }}!</span>
        <div class="text-subtitle-1 mt-2 pl-1">Let's make it parallel.</div>
        <!-- <div class="text-subtitle-2 text-right">— Somebody</div> -->
      </div>
    </div>

    <div class="text-h4 mt-15 font-weight-bold">💾 Documents</div>
    <v-alert type="info" class="mt-6" v-show="showAlert">
      There are no uploaded documents yet. Please upload some using the form
      below.
    </v-alert>
    <div class="mt-6">
      <v-row>
        <v-col cols="12" sm="6">
          <RawPanel @uploadFile="uploadFile" @onFileChange="onFileChange" @selectAndLoadPreview="selectAndLoadPreview"
            :info="LANGUAGES[langCodeFrom]" :items=items :isLoading=isLoading>
            </RawPanel>
        </v-col>
        <v-col cols="12" sm="6">
          <RawPanel @uploadFile="uploadFile" @onFileChange="onFileChange" @selectAndLoadPreview="selectAndLoadPreview"
            :info="LANGUAGES[langCodeTo]" :items=items :isLoading=isLoading>
            </RawPanel>
        </v-col>
      </v-row>
    </div>

    <div class="text-h4 mt-10 font-weight-bold">🔍 Preview</div>
    <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2">
      Documents are splitted by sentences using language specific rules.
    </v-alert>
    <v-row>
      <v-col v-for="(panel, i) in panels" :key="i" cols="12" sm="6">
        <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2" v-if="
            !splitted |
              !splitted[panel.langCode] |
              (splitted[panel.langCode].lines.length == 0)
          ">
          Select file to preview.
        </v-alert>
        <v-card v-else>
          <div class="yellow lighten-5">
            <v-card-title>{{ selected[panel.langCode] }}</v-card-title>
            <v-card-text>{{
                splitted[panel.langCode].meta.lines_count | separator
              }}
              lines</v-card-text>
          </div>
          <v-divider></v-divider>
          <div v-for="(line, i) in splitted[panel.langCode].lines" :key="i">
            <PreviewItem :item="line"></PreviewItem>
            <v-divider></v-divider>
          </div>
          <div class="text-center pa-3">
            <v-pagination v-model="splitted[panel.langCode].meta.page"
              :length="splitted[panel.langCode].meta.total_pages" total-visible="7" @input="
                onPreviewPageChange(
                  splitted[panel.langCode].meta.page,
                  panel.langCode
                )
              ">
            </v-pagination>
          </div>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn @click="downloadSplitted(panel.langCode)">Download</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <div class="text-h4 mt-10 font-weight-bold">⚖️ Alignment</div>
    <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2">
      This is a test version. Only {{DEFAULT_BATCHSIZE}} lines will be aligned.
    </v-alert>
    <v-row class="mt-6">
      <v-col v-for="(panel, i) in panels" :key="i" cols="12" sm="6">
        <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2"
          v-if="!selected[panel.langCode]">
          Select file to align.
        </v-alert>
        <v-card v-else>
          <div class="purple lighten-5">
            <v-card-title>{{ selected[panel.langCode] }}</v-card-title>
            <v-card-text>{{
                splitted[panel.langCode].meta.lines_count | separator
              }}
              lines</v-card-text>
          </div>
          <v-divider></v-divider>
          <v-simple-table>
            <template v-slot:default>
              <tbody>
                <tr>
                  <td>File</td>
                  <td>{{ selected[panel.langCode] }}</td>
                </tr>
                <tr>
                  <td>Lines</td>
                  <td>
                    {{ splitted[panel.langCode].meta.lines_count | separator }}
                  </td>
                </tr>
                <tr>
                  <td>Symbols</td>
                  <td>
                    {{
                      splitted[panel.langCode].meta.symbols_count | separator
                    }}
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>
      </v-col>
    </v-row>
    <v-btn v-show="selected['ru'] && selected['zh']" class="success mt-6" :loading="isLoading.align"
      :disabled="isLoading.align" @click="align()">
      Align documents
    </v-btn>

    <div class="text-h4 mt-10 font-weight-bold">✒️ Result</div>

    <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2"
      v-if="!itemsProcessing | (itemsProcessing['ru'].length == 0)">
      There are no previously aligned documents yet.
    </v-alert>

    <div v-else class="mt-6">
      <v-card>
        <div class="green lighten-5" dark>
          <v-card-title>Documents</v-card-title>
          <v-card-text>List of previosly aligned documents</v-card-text>
        </div>
        <v-divider></v-divider>
        <v-list class="pa-0">
          <v-list-item-group mandatory color="gray">
            <v-list-item v-for="(item, i) in itemsProcessing['ru']" :key="i" @change="selectProcessing('ru', item, i)">
              <v-list-item-icon>
                <v-icon>mdi-arrow-right</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="item"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-card>
      <div class="mt-5">
        <!-- <v-img :src="selectedProcessingImg" aspect-ratio="1" width="50%"></v-img> -->
        <v-img :src="selectedProcessingImgBest" aspect-ratio="1" width="50%"></v-img>
      </div>
      <v-card class="mt-6">
        <div class="green lighten-5" dark>
          <v-card-title>{{selectedProcessing}}</v-card-title>
          <v-card-text>Review and edit automatically aligned document</v-card-text>
        </div>
        <v-divider></v-divider>
        <div v-for="(line, i) in processing.items" :key="i">
          <EditItem :item="line"></EditItem>
          <v-divider></v-divider>
        </div>
        <div class="text-center pa-3">
          <v-pagination v-model="processing.meta.page" :length="processing.meta.total_pages" total-visible="10"
            @input="onProcessingPageChange(processing.meta.page)">
          </v-pagination>
        </div>
        <v-divider></v-divider>
        <v-card-actions>
          <v-row>
            <v-col class="py-0" cols="12" sm="6">
              <v-btn class="primary" @click="downloadProcessing('ru')">Download [ru]</v-btn>
            </v-col>
            <v-col class="py-0" cols="12" sm="6">
              <v-btn class="primary" @click="downloadProcessing('zh')">Download [zh]</v-btn>
            </v-col>
          </v-row>
        </v-card-actions>
      </v-card>
    </div>
  </div>
</template>

<script>
  import RawPanel from "@/components/RawPanel";
  import EditItem from "@/components/EditItem";
  import PreviewItem from "@/components/PreviewItem";
  import {
    mapGetters
  } from "vuex";
  import {
    DEFAULT_BATCHSIZE,
    API_URL
  } from "@/common/config";
  import {
    LANGUAGES,
    DEFAULT_FROM,
    DEFAULT_TO
  } from "@/common/langList";
  import {
    FETCH_ITEMS,
    FETCH_ITEMS_PROCESSING,
    UPLOAD_FILES,
    GET_SPLITTED,
    GET_ALIGNED,
    GET_PROCESSING,
    ALIGN_SPLITTED,
    DOWNLOAD_SPLITTED,
    DOWNLOAD_PROCESSING
  } from "@/store/actions.type";

  export default {
    data() {
      return {
        LANGUAGES,
        DEFAULT_FROM,
        DEFAULT_TO,
        DEFAULT_BATCHSIZE,
        panels: [{
            langCode: "ru",
            lang: "Russian",
            icon: "🥄"
          },
          {
            langCode: "zh",
            lang: "Chinese",
            icon: "🥢"
          }
        ],
        files: {
          ru: null,
          zh: null,
          de: null,
          en: null
        },
        selected: {
          ru: null,
          zh: null,
          de: null,
          en: null
        },
        selectedProcessing: null,
        selectedProcessingId: null,
        selectedIds: {
          ru: null,
          zh: null,
          de: null,
          en: null
        },
        isLoading: {
          upload: {
            ru: false,
            zh: false,
            de: false,
            en: false
          },
          align: false
        },
      };
    },
    methods: {
      onFileChange(file, langCode) {
        this.files[langCode] = file;
      },
      onPreviewPageChange(page, langCode) {
        this.$store.dispatch(GET_SPLITTED, {
          username: this.$route.params.username,
          langCode,
          fileId: this.selectedIds[langCode],
          linesCount: 10,
          page: page
        });
      },
      onProcessingPageChange(page) {
        this.$store.dispatch(GET_PROCESSING, {
          username: this.$route.params.username,
          fileId: this.selectedProcessingId,
          linesCount: 10,
          page: page
        });
      },
      uploadFile(langCode) {
        console.log("langcode =>", langCode)
        this.isLoading.upload[langCode] = true;
        this.$store
          .dispatch(UPLOAD_FILES, {
            file: this.files[langCode],
            username: this.$route.params.username,
            langCode
          })
          .then(() => {
            this.isLoading.upload[langCode] = false;
            this.selectFirstDocument(langCode);
          });
      },
      downloadSplitted(langCode) {
        this.$store.dispatch(DOWNLOAD_SPLITTED, {
          fileId: this.selectedIds[langCode],
          fileName: this.selected[langCode],
          username: this.$route.params.username,
          langCode
        });
      },
      downloadProcessing(langCode) {
        this.$store.dispatch(DOWNLOAD_PROCESSING, {
          fileId: this.selectedIds[langCode],
          fileName: this.selected[langCode],
          username: this.$route.params.username,
          langCode
        });
      },
      selectAndLoadPreview(langCode, name, fileId) {
        this.selected[langCode] = name;
        this.selectedIds[langCode] = fileId;
        this.$store.dispatch(GET_SPLITTED, {
          username: this.$route.params.username,
          langCode,
          fileId,
          linesCount: 10,
          page: 1
        });
        this.$store.dispatch(GET_ALIGNED, {
          username: this.$route.params.username,
          langCode,
          fileId,
          linesCount: 0
        });
      },
      selectProcessing(langCode, name, fileId) {
        if (langCode == "ru") {
          this.selectedProcessing = name;
          this.selectedProcessingId = fileId;
          this.$store.dispatch(GET_PROCESSING, {
            username: this.$route.params.username,
            fileId,
            linesCount: 10,
            page: 1
          });
        }
      },
      align() {
        this.isLoading.align = true;
        this.$store
          .dispatch(ALIGN_SPLITTED, {
            username: this.$route.params.username,
            fileIds: this.selectedIds
          })
          .then(() => {
            this.$store.dispatch(GET_PROCESSING, {
              username: this.$route.params.username,
              fileId: this.selectedIds["ru"],
              linesCount: 10,
              page: 1
            });
            this.$store.dispatch(FETCH_ITEMS_PROCESSING, {
              username: this.$route.params.username,
              langCode: 'ru'
            }).then(() => {
              this.selectFirstProcessingDocument("ru");
            });
            this.isLoading.align = false;
          });
      },
      //helpers
      itemsNotEmpty(langCode) {
        if (!this.items | !this.items[langCode]) {
          return true;
        }
        return this.items[langCode].length != 0;
      },
      itemsProcessingNotEmpty(langCode) {
        if (!this.itemsProcessing | !this.itemsProcessing[langCode]) {
          return false;
        }
        return this.itemsProcessing[langCode].length != 0;
      },
      selectFirstDocument(langCode) {
        if (this.itemsNotEmpty(langCode) & !this.selected[langCode]) {
          this.selectAndLoadPreview(langCode, this.items[langCode][0], 0);
        }
      },
      selectFirstProcessingDocument(langCode) {
        if (this.itemsProcessingNotEmpty(langCode)) {
          this.selectProcessing(langCode, this.itemsProcessing[langCode][0], 0);
        }
      }
    },
    mounted() {
      this.$store.dispatch(FETCH_ITEMS, {
        username: this.$route.params.username,
        langCode: this.langCodeFrom
      }).then(() => {
        this.selectFirstDocument(this.langCodeFrom);
      });
      this.$store.dispatch(FETCH_ITEMS, {
        username: this.$route.params.username,
        langCode: this.langCodeTo
      }).then(() => {
        this.selectFirstDocument(this.langCodeTo);
      });
      this.$store.dispatch(FETCH_ITEMS_PROCESSING, {
        username: this.$route.params.username,
        langCode: 'ru'
      }).then(() => {
        this.selectFirstProcessingDocument("ru");
      });
    },
    computed: {
      ...mapGetters(["items", "itemsProcessing", "splitted", "aligned", "processing"]),
      username() {
        return this.$route.params.username;
      },
      showAlert() {
        if (!this.items | !this.items.ru | !this.items.zh) {
          return true;
        }
        return (this.items.ru.length == 0) & (this.items.zh.length == 0);
      },
      selectedProcessingImg() {
        if (!this.selectedProcessing) {
          return "";
        }
        return `${API_URL}/static/img/${this.$route.params.username}/${this.selectedProcessing}.png`;
      },
      selectedProcessingImgBest() {
        if (!this.selectedProcessing) {
          return "";
        }
        return `${API_URL}/static/img/${this.$route.params.username}/${this.selectedProcessing}.best.png`;
      },
      langCodeFrom() {
        let langCode = this.$route.params.from;
        if (this.LANGUAGES[langCode]) {
          return langCode;
        }
        return DEFAULT_FROM;
      },
      langCodeTo() {
        let langCode = this.$route.params.to;
        if (this.LANGUAGES[langCode]) {
          return langCode;
        }
        return DEFAULT_TO;
      },
    },
    components: {
      EditItem,
      PreviewItem,
      RawPanel
    }
  };
</script>