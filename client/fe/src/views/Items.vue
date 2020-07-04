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
                    v-show="!splitted | !splitted[panel.langCode] | splitted[panel.langCode].length == 0">
                    Select file to preview.
                </v-alert>
                <v-list class="mt-2">
                    <v-list-item-group mandatory color="blue">
                        <v-list-item v-for="(line, i) in splitted[panel.langCode]" :key="i">
                            <v-list-item-content>
                                <v-list-item-title v-text="i+1 + '. ' + line"></v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-item-group>
                </v-list>
            </v-col>
        </v-row>

        <div class="text-h5 mt-10 font-weight-bold">Alignment</div>
        <v-row class="mt-6">
            <v-col v-for="(panel, i) in panels" :key=i cols="12" sm="6">
                <v-alert type="info" border="left" colored-border color="blue" class="mt-6" elevation="2"
                    v-show="!selected[panel.langCode]">
                    Document is not selected.
                </v-alert>
                <div v-show="selected[panel.langCode]">
                    <span class="font-weight-bold">Selected file</span>: {{selected[panel.langCode]}}
                </div>
            </v-col>
        </v-row>
        <div>
            <v-divider></v-divider>
            <v-btn class="success mt-10" @click="align()">Align documents</v-btn>
        </div>
    </div>
</template>

<script>
    import {
        mapGetters
    } from "vuex";

    import {
        FETCH_ITEMS,
        UPLOAD_FILES,
        GET_SPLITTED,
        ALIGN_SPLITTED
    } from "@/store/actions.type";

    export default {
        data() {
            return {
                panels: [{
                    langCode: "ru",
                    lang: "Russian",
                    img: "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
                    // img: "https://images.unsplash.com/photo-1568057374096-fb959e503fd2?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
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
            uploadFile(langCode) {
                this.$store.dispatch(UPLOAD_FILES, {
                    file: this.files[langCode],
                    username: this.$route.params.username,
                    langCode
                }).then(() => {
                    this.selectFirstDocument(langCode);
                });
            },
            selectAndLoadPreview(langCode, name, id) {
                this.selected[langCode] = name;
                this.selectedIds[langCode] = id;
                this.$store.dispatch(GET_SPLITTED, {
                    username: this.$route.params.username,
                    langCode,
                    fileId: id,
                    linesCount: 5
                });
            },
            align() {
                this.$store.dispatch(ALIGN_SPLITTED, {
                    username: this.$route.params.username,
                    fileIds: this.selectedIds
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
            ...mapGetters(["items", "splitted"]),
            username() {
                return this.$route.params.username
            },
            showAlert() {
                if (!this.items | !this.items.ru | !this.items.zh) {
                    return true
                }
                return this.items.ru.length == 0 & this.items.zh.length == 0
            }
        }
    }
</script>