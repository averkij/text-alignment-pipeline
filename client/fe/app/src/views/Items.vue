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
      <v-col cols="12" sm="6">
        <SplittedPanel @onPreviewPageChange="onPreviewPageChange" @downloadSplitted="downloadSplitted"
          :info="LANGUAGES[langCodeFrom]" :splitted=splitted :selected=selected>
        </SplittedPanel>
      </v-col>
      <v-col cols="12" sm="6">
        <SplittedPanel @onPreviewPageChange="onPreviewPageChange" @downloadSplitted="downloadSplitted"
          :info="LANGUAGES[langCodeTo]" :splitted=splitted :selected=selected>
        </SplittedPanel>
      </v-col>
    </v-row>

    <div class="text-h4 mt-10 font-weight-bold">⚖️ Alignment</div>
    <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2">
      This is a test version. Only {{TEST_LIMIT}} lines will be aligned.
    </v-alert>
    <v-row class="mt-6">
      <v-col cols="12" sm="6">
        <InfoPanel :info="LANGUAGES[langCodeFrom]" :splitted=splitted :selected=selected></InfoPanel>
      </v-col>
      <v-col cols="12" sm="6">
        <InfoPanel :info="LANGUAGES[langCodeTo]" :splitted=splitted :selected=selected></InfoPanel>
      </v-col>
    </v-row>
    <v-btn v-if="!userAlignInProgress" v-show="selected[langCodeFrom] && selected[langCodeTo]" class="success mt-6"
      :loading="isLoading.align" :disabled="isLoading.align" @click="align()">
      Align documents
    </v-btn>
    <v-btn v-else v-show="selected[langCodeFrom] && selected[langCodeTo]" class="error mt-6" @click="align()">
      Stop alignment
    </v-btn>

    <div class="text-h4 mt-10 font-weight-bold">✒️ Result</div>

    <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2"
      v-if="!itemsProcessing || !itemsProcessing[langCodeFrom] || (itemsProcessing[langCodeFrom].length == 0)">
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
            <v-list-item v-for="(item, i) in itemsProcessing[langCodeFrom]" :key="i"
              @change="selectProcessing(langCodeFrom, item, i)">
              <v-list-item-icon>
                <v-icon v-if="item.state[0]==PROC_INIT || item.state[0]==PROC_IN_PROGRESS" color="blue">
                  mdi-clock-outline</v-icon>
                <v-icon v-else-if="item.state[0]==PROC_ERROR" color="error">mdi-alert-circle</v-icon>
                <v-icon v-else color="teal">mdi-check</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="item.name"></v-list-item-title>
              </v-list-item-content>
              <v-progress-linear :value="item.state[2]/item.state[1] * 100" color="amber" :active="item.state[0]==PROC_INIT || item.state[0]==PROC_IN_PROGRESS" absolute bottom></v-progress-linear>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-card>

      <div class="text-h5 mt-10 font-weight-bold">Visualization</div>

      <v-alert v-if="!selectedProcessing || !selectedProcessing.imgs || selectedProcessing.imgs.length == 0" type="info" border="left" colored-border color="purple" class="mt-6" elevation="2" >
        Images will start showing after the first batch completion.
      </v-alert>
      <v-row v-else class="mt-6">
        <v-col v-for="(img, i) in selectedProcessing.imgs" :key=i cols="12" sm="3">
          <v-card>
            <div class="grey lighten-5">
              <v-card-title>
                batch {{i+1}}
                <v-spacer></v-spacer>
                <v-chip color="grey" text-color="black" small outlined>
                  {{DEFAULT_BATCHSIZE * i + 1}} — {{DEFAULT_BATCHSIZE * (i + 1)}}
                </v-chip>
              </v-card-title>
            </div>
            <v-divider></v-divider>
            <v-img :src="`${API_URL}/static/img/${username}/${img}`"
              :lazy-src="`${API_URL}/static/proc_img_stub.jpg`">
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular indeterminate color="green"></v-progress-circular>
                </v-row>
              </template>
            </v-img>
          </v-card>
        </v-col>
      </v-row>

      <div class="text-h5 mt-10 font-weight-bold">Edit</div>

      <v-alert v-if="!processing || !processing.items || processing.items.length == 0" type="info" border="left" colored-border color="info" class="mt-6" elevation="2" >
        Please, wait. Alignment is in progress.
      </v-alert>
      <v-card v-else class="mt-6">
        <div class="green lighten-5" dark>
          <v-card-title class="pr-3">
            {{selectedProcessing.name}}
            <v-spacer></v-spacer>
            <v-btn icon @click="collapseEditItems">
              <v-icon>mdi-collapse-all</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>Review and edit automatically aligned document</v-card-text>
        </div>
        <v-divider></v-divider>
        <div v-for="(line, i) in processing.items" :key="i">
          <EditItem @editProcessing="editProcessing" :item="line" :collapse="triggerCollapseEditItem"></EditItem>
          <v-divider></v-divider>
        </div>
        <div class="text-center pa-3">
          <v-pagination v-model="processing.meta.page" :length="processing.meta.total_pages" total-visible="10"
            @input="onProcessingPageChange(processing.meta.page)">
          </v-pagination>
        </div>
      </v-card>

      <div class="text-h4 mt-10 font-weight-bold">🧲 Download</div>

      <div class="mt-5">
        <v-btn class="primary ma-5" @click="downloadProcessing(langCodeFrom)">Download [{{langCodeFrom}}]</v-btn>
        <v-btn class="primary ma-5" @click="downloadProcessing(langCodeTo)">Download [{{langCodeTo}}]</v-btn>
        <v-btn class="primary ma-5" @click="downloadProcessingTmx()">Download TMX</v-btn>
      </div>

    </div>
  </div>
</template>

<script>
  import RawPanel from "@/components/RawPanel";
  import SplittedPanel from "@/components/SplittedPanel";
  import InfoPanel from "@/components/InfoPanel";
  import EditItem from "@/components/EditItem";
  import {
    mapGetters
  } from "vuex";
  import {
    DEFAULT_BATCHSIZE,
    TEST_LIMIT,
    API_URL
  } from "@/common/config";
  import {
    LANGUAGES,
    DEFAULT_FROM,
    DEFAULT_TO
  } from "@/common/langList";
  import {
    RESULT_OK,
    RESULT_ERROR,
    PROC_INIT,
    PROC_IN_PROGRESS,
    PROC_DONE,
    PROC_ERROR,
  } from "@/common/constants"
  import {
    FETCH_ITEMS,
    FETCH_ITEMS_PROCESSING,
    UPLOAD_FILES,
    GET_SPLITTED,
    GET_PROCESSING,
    EDIT_PROCESSING,
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
        TEST_LIMIT,
        API_URL,
        PROC_INIT,
        PROC_IN_PROGRESS,
        PROC_ERROR,
        PROC_DONE,
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
        triggerCollapseEditItem: false,
        userAlignInProgress: false
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
        this.triggerCollapseEditItem = !this.triggerCollapseEditItem;
        this.$store.dispatch(GET_PROCESSING, {
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          fileId: this.selectedProcessingId,
          linesCount: 10,
          page: page
        });
      },
      uploadFile(langCode) {
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
          fileId: this.selectedIds[this.langCodeFrom],
          fileName: this.selected[this.langCodeFrom],
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          langCodeDownload: langCode,
          format: "txt"
        });
      },
      downloadProcessingTmx() {
        this.$store.dispatch(DOWNLOAD_PROCESSING, {
          fileId: this.selectedIds[this.langCodeFrom],
          fileName: this.selected[this.langCodeFrom] + ".tmx",
          username: this.$route.params.username,
          langCodeFrom: this.langCodeFrom,
          langCodeTo: this.langCodeTo,
          langCodeDownload: this.langCodeFrom,
          format: "tmx"
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
      },
      selectProcessing(langCode, item, fileId) {
        if (langCode == this.langCodeFrom) {
          this.selectedProcessing = item;
          this.selectedProcessingId = fileId;
          this.$store.dispatch(GET_PROCESSING, {
            username: this.$route.params.username,
            langCodeFrom: this.langCodeFrom,
            langCodeTo: this.langCodeTo,
            fileId,
            linesCount: 10,
            page: 1
          });
        }
      },
      editProcessing(line_id, text, text_type, callback) {
        this.$store
          .dispatch(EDIT_PROCESSING, {
            username: this.$route.params.username,
            fileId: this.selectedProcessingId,
            langCodeFrom: this.langCodeFrom,
            langCodeTo: this.langCodeTo,
            line_id: line_id,
            text: text,
            text_type: text_type
          }).then(function () {
            callback(RESULT_OK)
          }).catch(() => {
            callback(RESULT_ERROR)
          });
      },
      align() {
        this.isLoading.align = true;
        this.$store
          .dispatch(ALIGN_SPLITTED, {
            username: this.$route.params.username,
            fileIds: this.selectedIds,
            langCodeFrom: this.langCodeFrom,
            langCodeTo: this.langCodeTo
          })
          .then(() => {
            this.userAlignInProgress = true;
            this.isLoading.align = false;

            this.$store.dispatch(FETCH_ITEMS_PROCESSING, {
              username: this.$route.params.username,
              langCodeFrom: this.langCodeFrom,
              langCodeTo: this.langCodeTo
            }).then(() => {
              this.selectFirstProcessingDocument(this.langCodeFrom);
            });

            this.fetchItemsProvessingTimer();
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
      },
      collapseEditItems() {
        this.triggerCollapseEditItem = !this.triggerCollapseEditItem;
      },
      fetchItemsProvessingTimer() {
        setTimeout(() => {
          this.$store.dispatch(FETCH_ITEMS_PROCESSING, {
              username: this.$route.params.username,
              langCodeFrom: this.langCodeFrom,
              langCodeTo: this.langCodeTo
            }).then(() => {
              if (this.itemsProcessing[this.langCodeFrom].filter(x => x.state[0] == 0 || x.state[0] == 1).length > 0) {
                this.userAlignInProgress = true;
                this.fetchItemsProvessingTimer();
              }
              else {
                this.userAlignInProgress = false;
                this.selectFirstProcessingDocument(this.langCodeFrom);
              }
              this.selectProcessing(this.langCodeFrom, this.itemsProcessing[this.langCodeFrom][0], 0)
            });
        }, 5000)
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
        langCodeFrom: this.langCodeFrom,
        langCodeTo: this.langCodeTo
      }).then(() => {
        if (this.itemsProcessing[this.langCodeFrom].filter(x => x.state[0] == 0 || x.state[0] == 1).length > 0) {
          this.userAlignInProgress = true;
          this.fetchItemsProvessingTimer();
        }
        this.selectFirstProcessingDocument(this.langCodeFrom);
      });
    },
    computed: {
      ...mapGetters(["items", "itemsProcessing", "splitted", "processing"]),
      username() {
        return this.$route.params.username;
      },
      showAlert() {
        if (!this.items | !this.items[this.langCodeFrom] | !this.items[this.langCodeTo]) {
          return true;
        }
        return (this.items[this.langCodeFrom].length == 0) & (this.items[this.langCodeTo].length == 0);
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
      RawPanel,
      SplittedPanel,
      InfoPanel
    }
  };
</script>