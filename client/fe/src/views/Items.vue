<template>

    <div>
        <div class="text-h3 mt-5">Hello, {{username}}!</div>
        <div class="text-h5 mt-15 font-weight-bold">Documents</div>

        <v-alert type="info" class="mt-6" v-show="showAlert">
            There are no uploaded documents yet. Please upload some using the form below.
        </v-alert>

        <div class="mt-6">
            <v-row>
                <v-col v-for="(panel, i) in panels" :key=i cols="12" sm="6">
                    <v-card>
                        <v-img position="top" class="white--text" height="200px" :src="panel.img">
                            <v-card-title>{{panel.lang}}</v-card-title>
                        </v-img>
                        <v-list class="pa-0">
                            <v-list-item-group mandatory color="blue">
                                <v-list-item v-for="(item, i) in items[panel.langCode]" :key="i"
                                    @change="selectAndLoadPreview(panel.langCode, item, i)">
                                    <v-list-item-icon>
                                        <v-icon>mdi-star</v-icon>
                                    </v-list-item-icon>
                                    <v-list-item-content>
                                        <v-list-item-title v-text="item"></v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-list-item-group>
                        </v-list>
                        <v-divider></v-divider>
                        <v-card-title>Upload</v-card-title>
                        <v-card-text>Upload raw {{panel.lang}} document in txt format.</v-card-text>
                        <v-card-actions>
                            <v-file-input outlined dense accept=".txt" @change="onFileChange($event,panel.langCode)">
                            </v-file-input>
                        </v-card-actions>
                        <v-divider></v-divider>
                        <v-card-actions>
                            <v-btn @click="uploadFile(panel.langCode)">Upload</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </div>

        <div class="text-h5 mt-10 font-weight-bold">Preview</div>
        <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2">
            Documents are splitted by sentences using language specific rules.
        </v-alert>
        <v-row>
            <v-col v-for="(panel, i) in panels" :key=i cols="12" sm="6">
                <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2"
                    v-show="!splitted | !splitted[panel.langCode] | splitted[panel.langCode].lines.length == 0">
                    Select file to preview.
                </v-alert>
                <div v-for="(line, i) in splitted[panel.langCode].lines" :key="i">
                    <PreviewItem :item="line"></PreviewItem>
                    <v-divider></v-divider>
                </div>
                <div class="text-center mt-3">
                    <v-pagination v-model="splitted[panel.langCode].meta.page"
                        :length="splitted[panel.langCode].meta.total_pages" total-visible="7"
                        @input="onPreviewPageChange(splitted[panel.langCode].meta.page, panel.langCode)">
                    </v-pagination>
                </div>
            </v-col>
        </v-row>

        <div class="text-h5 mt-10 font-weight-bold">Alignment</div>
        <v-row class="mt-6">
            <v-col v-for="(panel, i) in panels" :key=i cols="12" sm="6">
                <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2"
                    v-show="!selected[panel.langCode]">
                    Document is not selected.
                </v-alert>
                <v-simple-table v-show="selected[panel.langCode]">
                    <template v-slot:default>
                        <tbody>
                            <tr>
                                <td>File</td>
                                <td>{{selected[panel.langCode]}}</td>
                            </tr>
                            <tr>
                                <td>Lines</td>
                                <td>{{splitted[panel.langCode].meta.lines_count | separator}}</td>
                            </tr>
                            <tr>
                                <td>Symbols</td>
                                <td>{{splitted[panel.langCode].meta.symbols_count | separator}}</td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </v-col>
        </v-row>
        <div>
            <v-btn class="success mt-10" @click="align()">Align documents</v-btn>
        </div>

        <div class="text-h5 mt-10 font-weight-bold">Edit</div>

        <div class="mt-10">
            <div v-for="(line,i) in processing.items" :key="i">
                <EditItem :item="line"></EditItem>
                <v-divider></v-divider>
            </div>
            <div class="text-center mt-3">
                <v-pagination v-model="processing.meta.page" :length="processing.meta.total_pages" total-visible="10"
                    @input="onProcessingPageChange(processing.meta.page)">
                </v-pagination>
            </div>
        </div>

        <!-- <v-row v-show="processing.length > 0">
            <v-col cols="12" sm="6">
                <v-list class="mt-2">
                    <v-list-item-group mandatory color="blue">
                        <v-list-item v-for="(line, i) in processing" :key="i">
                            <v-list-item-content>
                                <v-list-item-title v-text="line.line_ids + '. ' + line.text"></v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-item-group>
                </v-list>
            </v-col>
            <v-col cols="12" sm="6">
                <v-list class="mt-2">
                    <v-list-group v-for="(line, i) in processing" :key="i" mandatory color="blue">
                        <template v-slot:activator>
                            <v-list-item-content>
                                <v-list-item-title v-text="line.trans[0].line_ids + '. ' + line.trans[0].text">
                                </v-list-item-title>
                            </v-list-item-content>
                        </template>
                        <v-list-item v-for="tran in line.trans" :key="tran.sim">
                            <v-list-item-content>
                                <v-list-item-title class="pl-5"
                                    v-text="tran.line_ids + '. ' + tran.text + ' (' + tran.sim + ')'">
                                </v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-group>
                </v-list>
            </v-col>
        </v-row> -->

        <div class="text-h5 mt-10 font-weight-bold">Result</div>
        <v-row>
            <v-col v-for="(panel, i) in panels" :key=i cols="12" sm="6">
                <v-list class="mt-2">
                    <v-list-item-group mandatory color="blue">
                        <v-list-item v-for="(line, i) in aligned[panel.langCode]" :key="i">
                            <v-list-item-content>
                                <v-list-item-title v-text="i+1 + '. ' + line"></v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-item-group>
                </v-list>
            </v-col>
        </v-row>
    </div>
</template>

<script>
    import EditItem from "@/components/EditItem"
    import PreviewItem from "@/components/PreviewItem"
    import {
        mapGetters
    } from "vuex";

    import {
        FETCH_ITEMS,
        UPLOAD_FILES,
        GET_SPLITTED,
        GET_ALIGNED,
        GET_PROCESSING,
        ALIGN_SPLITTED
    } from "@/store/actions.type";

    export default {
        data() {
            return {
                panels: [{
                    langCode: "ru",
                    lang: "Russian",
                    img: "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
                }, {
                    langCode: "zh",
                    lang: "Chinese",
                    img: "https://images.unsplash.com/photo-1538099023053-30e7da644196?ixlib=rb-1.2.1&&auto=format&fit=crop&w=1350&q=80"
                }],
                files: {
                    "ru": null,
                    "zh": null
                },
                selected: {
                    "ru": null,
                    "zh": null
                },
                selectedIds: {
                    "ru": null,
                    "zh": null
                }
            }
        },
        methods: {
            onFileChange(file, langCode) {
                this.files[langCode] = file
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
                    fileId: this.selectedIds['ru'],
                    linesCount: 10,
                    page: page
                });
            },
            uploadFile(langCode) {
                this.$store.dispatch(UPLOAD_FILES, {
                    file: this.files[langCode],
                    username: this.$route.params.username,
                    langCode
                }).then(() => {
                    this.selectFirstDocument(langCode);
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
                if (langCode == "ru") {
                    this.$store.dispatch(GET_PROCESSING, {
                        username: this.$route.params.username,
                        fileId,
                        linesCount: 10,
                        page: 1
                    });
                }
            },
            align() {
                this.$store.dispatch(ALIGN_SPLITTED, {
                    username: this.$route.params.username,
                    fileIds: this.selectedIds
                }).then(() => {
                    this.$store.dispatch(GET_ALIGNED, {
                        username: this.$route.params.username,
                        langCode: "ru",
                        fileId: this.selectedIds["ru"],
                        linesCount: 0
                    });
                    this.$store.dispatch(GET_ALIGNED, {
                        username: this.$route.params.username,
                        langCode: "zh",
                        fileId: this.selectedIds["zh"],
                        linesCount: 0
                    });
                });
            },
            //helpers
            itemsNotEmpty(langCode) {
                if (!this.items | !this.items[langCode]) {
                    return true
                }
                return this.items[langCode].length != 0
            },
            selectFirstDocument(langCode) {
                if (this.itemsNotEmpty(langCode) & !this.selected[langCode]) {
                    this.selectAndLoadPreview(langCode, this.items[langCode][0], 0);
                }
            }
        },
        mounted() {
            this.$store.dispatch(FETCH_ITEMS, this.$route.params.username).then(() => {
                this.selectFirstDocument("ru");
                this.selectFirstDocument("zh");
            });
        },
        computed: {
            ...mapGetters(["items", "splitted", "aligned", "processing"]),
            username() {
                return this.$route.params.username
            },
            showAlert() {
                if (!this.items | !this.items.ru | !this.items.zh) {
                    return true
                }
                return this.items.ru.length == 0 & this.items.zh.length == 0
            }
        },
        components: {
            EditItem,
            PreviewItem
        }
    }
</script>