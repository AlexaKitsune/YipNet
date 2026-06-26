<template>
    <div class="PostComments-MAIN mt-4 space-y-4 border-t border-white/10 pt-4">
        <div v-if="replyingTo" class="mb-2 rounded bg-black/30 p-2 text-sm">
            {{ $t('postComments.replyingTo') }} @{{ replyingTo.at_sign || replyingTo.nickname }}
            <UButton size="xs" variant="ghost" @click="replyingTo = null">
                <b>{{ $t('postComments.btnCancelReply') }}</b>
            </UButton>
        </div>
        <UTextarea
            v-model="commentText"
            :placeholder="$t('postComments.writeAComment')"
            autoresize
            :rows="2"
            :disabled="loading"
            class="w-full"
            :ui="{ base: 'w-full bg-black text-white placeholder:text-gray-500' }"
        />
        <div v-if="previewActive && commentText.trim()" class="mt-4 max-h-64 overflow-y-auto rounded-md bg-black/30 p-3"> <AlexiconMarkdown :val="commentText" /> </div>

        <!-- preview media -->
        <div v-if="filesInput.files.length" class="rounded-lg bg-black/20 p-3 space-y-3">
            <div v-if="mediaFiles.length" class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2">
                <div v-for="(item, index) in mediaFiles" :key="index" class="overflow-hidden rounded-md bg-black/30">
                    <img v-if="item.type.startsWith('image/')" :src="item.url" class="size-20 w-full object-cover">
                    <video v-else-if="item.type.startsWith('video/')" class="size-20 w-full object-cover">
                        <source :src="item.url + '#t=1'" :type="item.type">
                    </video>
                </div>
            </div>
            
            <div v-if="otherFiles.length" class="space-y-1">
                <div v-for="(item, index) in otherFiles" :key="index" class="flex items-center gap-2 rounded-md bg-black/20 px-2 py-1 text-sm opacity-80">
                    <UIcon name="i-lucide-file" />
                    <span class="truncate">{{ item.name }}</span>
                </div>
            </div>
        </div>

        <!-- actions -->
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div class="flex flex-wrap items-center gap-3">
                <label class="files-input">
                    <UButton icon="i-lucide-paperclip" variant="ghost" color="neutral" />
                    <input
                        type="file"
                        multiple
                        @change="setFilesPreview"
                        ref="post-files-input"
                        :disabled="loading"
                    >
                </label>

                <UButton
                    icon="i-lucide-trash-2"
                    variant="ghost"
                    color="neutral"
                    :disabled="loading || !filesInput.files.length"
                    @click="deleteFiles"
                />

                <label class="flex items-center gap-2 text-sm whitespace-nowrap">
                    <USwitch v-model="aiGenerated" :disabled="loading" />
                    <span>{{ $t('postComments.aiGenerated') }}</span>
                </label>
                <label class="flex items-center gap-2 text-sm whitespace-nowrap">
                    <USwitch v-model="previewActive"/> <span>{{ $t('postComments.preview') }}</span>
                </label>
            </div>

            <UButton
                color="primary"
                :loading="loading"
                :disabled="!commentText.trim() || loading"
                @click="submitComment"
            >
                {{ $t('postComments.btnComment') }}
            </UButton>
        </div>

        <USeparator/>

        <!-- view comments -->
        <div class="space-y-3">
            <CommentRenderer
                v-for="comment in commentTree"
                :key="comment.id"
                :comment-data="comment"
                :depth="0"
                @reply="replyingTo = $event"
                @deleted="removeComment"
            />
        </div>

    </div>
</template>

<script>
const API_URL = import.meta.env.VITE_API_URL
import { getComments, createComment } from '@/services/yipnet/comments.js'
import { uploadFile } from '@/services/alexicon/media.js'
import { putVote, deleteVote } from '@/services/yipnet/votes.js'
import AlexiconMarkdown from '@/components/AlexiconMarkdown.vue'
import AlexiconMasonry from './AlexiconMasonry.vue'
import AlexiconDoc from './AlexiconDoc.vue'
import ContentOptionsMenu from './ContentOptionsMenu.vue'
import CommentRenderer from './CommentRenderer.vue'

export default {
    name: 'PostComments',
    components: {
        AlexiconMarkdown, AlexiconMasonry, AlexiconDoc, ContentOptionsMenu, CommentRenderer,
    },
    props: {
        postId: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            comments: [],
            commentText: '',
            loading: false,
            aiGenerated: false,
            filesInput: {
                files: []
            },
            uploadedFilesArray: [],
            previewActive: false,
            replyingTo: null,
        }
    },
    methods: {
        setFilesPreview(event) {
            const files = event.target.files

            for (const file of files) {
                if (this.filesInput.files.length >= 50) return;

                const isMedia =
                    file.type.startsWith('image/') ||
                    file.type.startsWith('video/');

                this.filesInput.files.push({
                    file,
                    url: isMedia ? URL.createObjectURL(file) : null,
                    type: file.type,
                    isMedia,
                    name: file.name
                });
            }
        },

        deleteFiles() {
            if (this.loading) return;

            for (const item of this.filesInput.files) {
                if (item.url) URL.revokeObjectURL(item.url);
            }

            this.filesInput.files = [];

            const input = this.$refs['post-files-input']
            if (input) {
                input.value = '';
            }
        },

        async loadComments() {
            const result = await getComments(this.postId)
            this.comments = result.data.comments || []
        },

        async submitComment() {
            this.loading = true
            this.uploadedFilesArray = []

            try {
                const files = this.filesInput.files.map(item => item.file)

                if (files.length) {
                    const userId = localStorage.getItem('alexicon_user_id')
                    const targetPath = `yipnet/${userId}/comments/`

                    const results = await Promise.all(
                        files.map(file => uploadFile(file, {
                            targetPath,
                            visibility: 'public'
                        }))
                    )

                    this.uploadedFilesArray = results
                        .map(item => item.fileId || item.id || item.data?.fileId || item.data?.id)
                        .filter(Boolean)
                }

                await createComment(this.postId, {
                    content: this.commentText,
                    media: this.uploadedFilesArray,
                    ai_generated: this.aiGenerated,
                    parent_id: this.replyingTo?.id || null
                })

                this.resetCommentForm()
                await this.loadComments()
            } finally {
                this.loading = false
            }
        },

        resetCommentForm() {
            this.commentText = ''
            this.aiGenerated = false
            this.previewActive = false
            this.uploadedFilesArray = []
            this.replyingTo = null

            for (const item of this.filesInput.files) {
                if (item.url) {
                    URL.revokeObjectURL(item.url)
                }
            }

            this.filesInput.files = []

            const input = this.$refs['post-files-input']
            if (input) {
                input.value = ''
            }
        },

        removeComment(payload) {
            this.comments = this.comments.filter(comment => {
                return Number(comment.id) !== Number(payload.id)
            })
        },
    },
    mounted() {
        this.loadComments()
    },
    computed: {
        mediaFiles() {
            return this.filesInput.files.filter(item => item.isMedia);
        },

        otherFiles() {
            return this.filesInput.files.filter(item => !item.isMedia);
        },

        commentTree() {
            const map = new Map()
            const roots = []

            for (const comment of this.comments) {
                map.set(comment.id, {
                    ...comment,
                    replies: []
                })
            }

            for (const comment of map.values()) {
                if (comment.parent_id && map.has(comment.parent_id)) {
                    map.get(comment.parent_id).replies.push(comment)
                } else {
                    roots.push(comment)
                }
            }

            return roots
        },
    },
    beforeUnmount() {
        for (const item of this.filesInput.files) {
            if (item.url) {
                URL.revokeObjectURL(item.url)
            }
        }
    }
}
</script>

<style scoped lang="stylus">
.files-input
    position relative
    display inline-block

    input[type="file"]
        position absolute
        top 0
        left 0
        width 100%
        height 100%
        opacity 0
        cursor pointer
</style>