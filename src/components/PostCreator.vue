<template>
<UModal
    :open="true"
    @update:open="close"
    :ui="{ content: 'max-w-[760px] w-[min(92vw,760px)] overflow-visible bg-transparent ring-0 shadow-none', overlay: 'bg-black/60 backdrop-blur-sm' }"
    class="PostCreator-MAIN"
>
	<template #content>
        <UCard
            class="w-full max-h-[85vh] overflow-y-auto bg-[var(--alexicon-surface)] text-[var(--alexicon-text)] shadow-[0_0_1ch_rgba(0,0,0,0.45)] border-0"
            :ui="{ root: 'border-0', header: 'border-0', body: 'border-0', footer: 'border-0'}"
            variant="ghost"
        >
			<template #header>
				<div class="flex items-center justify-between">
					<h1 class="text-xl font-bold">{{ $t('postCreator.createPost') }}</h1>
					<UButton icon="i-lucide-x" variant="ghost" color="neutral" @click="close"/>
				</div>
			</template>

            <div class="textarea-wrap">
                <UTextarea
                    ref="postTextarea"
                    v-model="postText"
                    autoresize
                    :rows="4"
                    :placeholder="$t('postCreator.placeholderContent')"
                    :disabled="uploading"
                    class="w-full"
                    :ui="{ base: 'min-h-32 max-h-64 resize-y bg-black text-white placeholder:text-gray-500' }"
                    @input="handleMentionInput"
                    @keyup="handleMentionInput"
                    @keydown.down.prevent="moveMentionSelection(1)"
                    @keydown.up.prevent="moveMentionSelection(-1)"
                    @keydown.enter.prevent="selectActiveMention"
                    @keydown.esc="closeMentionDropdown"
                />

                <div
                    v-if="mentionDropdownOpen && mentionUsers.length"
                    class="mention-dropdown"
                >
                    <button
                        v-for="(user, index) in mentionUsers"
                        :key="user.id"
                        class="mention-item"
                        :class="{ 'mention-item-active': index === mentionSelectedIndex }"
                        type="button"
                        @mousedown.prevent="insertMention(user)"
                    >
                        <UAvatar :src="userAvatar(user.profile_pic)" size="xs" />

                        <div class="min-w-0 text-left">
                            <p class="truncate font-semibold">
                                {{ user.name }} {{ user.surname }}
                            </p>

                            <p class="truncate text-xs opacity-60">
                                @{{ user.at_sign || user.nickname }}
                            </p>
                        </div>
                    </button>
                </div>
            </div>

            <div v-if="previewActive && postText.trim()" class="mt-4 max-h-64 overflow-y-auto rounded-md bg-black/30 p-3">
                <AlexiconMarkdown :val="postText" />
            </div>

			<div v-if="filesInput.files.length" class="mt-4 space-y-3">
				<div class="flex gap-2 overflow-x-auto">
					<div v-for="(item, index) in mediaFiles" :key="index" class="shrink-0">
						<img v-if="item.type.startsWith('image/')" :src="item.url" class="size-24 rounded-md object-cover bg-black/20">
						<video v-else-if="item.type.startsWith('video/')" class="size-24 rounded-md object-cover bg-black/20">
							<source :src="item.url + '#t=1'" :type="item.type">
						</video>
					</div>
				</div>

				<div v-if="otherFiles.length" class="space-y-1">
					<div v-for="(item, index) in otherFiles" :key="index" class="flex items-center gap-2 text-sm opacity-80">
						<UIcon name="i-lucide-file" />
						<span>{{ item.name }}</span>
					</div>
				</div>
			</div>

			<template #footer>
                <div class="flex flex-col gap-4">
                    <div class="flex flex-wrap items-center gap-x-6 gap-y-4">
                        <div class="flex items-center gap-3">
                            <label class="files-input">
                                <UButton icon="i-lucide-paperclip" variant="ghost" color="neutral"/>
                                <input type="file" multiple @change="setFilesPreview" ref="post-files-input" :disabled="uploading">
                            </label>

                            <UButton icon="i-lucide-trash-2" variant="ghost" color="neutral" @click="deleteFiles" />
                        </div>

                        <label class="flex items-center gap-2 text-sm whitespace-nowrap">
                            <USwitch v-model="privatePost"/> <span>{{ $t('postCreator.private') }}</span>
                        </label>

                        <label class="flex items-center gap-2 text-sm whitespace-nowrap">
                            <USwitch v-model="nsfwPost"/> <span>NSFW</span>
                        </label>

                        <label class="flex items-center gap-2 text-sm whitespace-nowrap">
                            <USwitch v-model="aiGenerated"/> <span>{{ $t('postCreator.aiGenerated') }}</span>
                        </label>

                        <label class="flex items-center gap-2 text-sm whitespace-nowrap">
                            <USwitch v-model="previewActive"/> <span><b>{{ $t('postCreator.preview') }}</b></span>
                        </label>

                        <UAlert
                            v-if="errorMessage"
                            color="error"
                            variant="soft"
                            icon="i-lucide-triangle-alert"
                            :title="errorMessage"
                            class="mb-4"
                        />

                        <UButton class="w-full mt-2 items-center justify-center" color="primary" :loading="uploading" :disabled="!postText.trim() || uploading" @click="post">
                            {{ $t('postCreator.btnPost') }}
                        </UButton>
                    </div>
                </div>
            </template>
		</UCard>
	</template>
</UModal>
</template>

<script>
const API_URL = import.meta.env.VITE_API_URL

import { createPost } from '@/services/yipnet/posts'
import { uploadFile } from '@/services/alexicon/media'
import { getMentionSuggestions } from '@/services/alexicon/social'
import AlexiconMarkdown from '@/components/AlexiconMarkdown.vue'

export default {
    name: 'PostCreator',

    emits: ['close', 'update-post'],

    components: {
        AlexiconMarkdown,
    },

    data() {
        return {
            postText: '',
            filesInput: {
                files: []
            },
            privatePost: false,
            nsfwPost: false,
            aiGenerated: false,
            previewActive: false,
            uploading: false,
            uploadedFilesArray: [],
            errorMessage: '',

            mentionDropdownOpen: false,
            mentionUsers: [],
            mentionQuery: '',
            mentionStartIndex: null,
            mentionSelectedIndex: 0,
            mentionTimer: null,
        }
    },

    computed: {
        mediaFiles() {
            return this.filesInput.files.filter(item => item.isMedia);
        },

        otherFiles() {
            return this.filesInput.files.filter(item => !item.isMedia);
        }
    },

    methods: {
        userAvatar(value) {
            if (!value) return ''

            if (String(value).startsWith('/')) {
                return `${API_URL}${value}`
            }

            return `${API_URL}/alexicon/media/${value}`
        },

        getTextareaElement() {
            const ref = this.$refs.postTextarea

            return ref?.textarea || ref?.$el?.querySelector('textarea') || null
        },

        getActiveMention() {
            const textarea = this.getTextareaElement()
            const cursor = textarea?.selectionStart ?? this.postText.length
            const beforeCursor = this.postText.slice(0, cursor)

            const match = beforeCursor.match(/(^|\s)@([a-zA-Z0-9_]{1,32})$/)

            if (!match) return null

            const query = match[2]
            const startIndex = cursor - query.length - 1

            return {
                query,
                startIndex,
                endIndex: cursor
            }
        },

        handleMentionInput() {
            clearTimeout(this.mentionTimer)

            const activeMention = this.getActiveMention()

            if (!activeMention) {
                this.closeMentionDropdown()
                return
            }

            this.mentionQuery = activeMention.query
            this.mentionStartIndex = activeMention.startIndex

            this.mentionTimer = setTimeout(() => {
                this.loadMentionSuggestions()
            }, 200)
        },

        async loadMentionSuggestions() {
            if (!this.mentionQuery) {
                this.closeMentionDropdown()
                return
            }

            try {
                const result = await getMentionSuggestions(this.mentionQuery)

                this.mentionUsers = result.data?.users || result.users || []
                this.mentionDropdownOpen = this.mentionUsers.length > 0
                this.mentionSelectedIndex = 0
            } catch (error) {
                console.error(error)
                this.closeMentionDropdown()
            }
        },

        moveMentionSelection(direction) {
            if (!this.mentionDropdownOpen || !this.mentionUsers.length) return

            const total = this.mentionUsers.length

            this.mentionSelectedIndex =
                (this.mentionSelectedIndex + direction + total) % total
        },

        selectActiveMention() {
            if (!this.mentionDropdownOpen || !this.mentionUsers.length) {
                this.post()
                return
            }

            this.insertMention(this.mentionUsers[this.mentionSelectedIndex])
        },

        insertMention(user) {
            const textarea = this.getTextareaElement()
            const cursor = textarea?.selectionStart ?? this.postText.length
            const tag = user.at_sign || user.nickname

            if (!tag || this.mentionStartIndex === null) return

            const before = this.postText.slice(0, this.mentionStartIndex)
            const after = this.postText.slice(cursor)

            this.postText = `${before}@${tag} ${after}`

            this.closeMentionDropdown()

            this.$nextTick(() => {
                const el = this.getTextareaElement()
                const newCursor = before.length + tag.length + 2

                if (el) {
                    el.focus()
                    el.setSelectionRange(newCursor, newCursor)
                }
            })
        },

        closeMentionDropdown() {
            this.mentionDropdownOpen = false
            this.mentionUsers = []
            this.mentionQuery = ''
            this.mentionStartIndex = null
            this.mentionSelectedIndex = 0
        },

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
            if (this.uploading) return;

            for (const item of this.filesInput.files) {
                if (item.url) URL.revokeObjectURL(item.url);
            }

            this.filesInput.files = [];

            const input = this.$refs['post-files-input']

            if (input) {
                input.value = '';
            }
        },

        async post() {
            this.uploading = true;
            this.errorMessage = '';
            this.uploadedFilesArray = [];

            try {
                const files = this.filesInput.files.map(item => item.file);

                if (files.length) {
                    const userId = localStorage.getItem('alexicon_user_id');
                    const targetPath = `yipnet/${userId}/`;
                    const visibility = this.privatePost ? 'private' : 'public';

                    const results = await Promise.all(
                        files.map(file => uploadFile(file, {
                            targetPath,
                            visibility
                        }))
                    );
                    
                    this.uploadedFilesArray = results.map(item => item.data?.fileId).filter(Boolean);
                }

                await this.finallyPost();
            } catch (error) {
                console.error(error);
                this.errorMessage = error.message || 'Error al subir archivos.';
            } finally {
                this.uploading = false;
            }
        },

        async finallyPost() {
            const newPost = {
                content: this.postText,
                media: this.uploadedFilesArray,
                sharing_id: null,
                private_post: this.privatePost,
                nsfw_post: this.nsfwPost,
                ai_generated: this.aiGenerated
            };

            const result = await createPost(newPost);

            if (result.status !== 'success') {
                this.errorMessage = 'Failed to create post. Please try again.';
                return;
            }

            this.$emit('update-post');
            this.$emit('close');
        },

        close() {
            this.deleteFiles();
            this.$emit('close');
        }
    },

    beforeUnmount() {
        clearTimeout(this.mentionTimer)
        this.deleteFiles();
    }
}
</script>

<style scoped lang="stylus">
.textarea-wrap
    position relative

.mention-dropdown
    position absolute
    left 0
    right 0
    top calc(100% + 0.35rem)
    z-index 9999
    max-height 260px
    overflow-y auto
    border-radius 10px
    background #111
    box-shadow 0 0 1ch rgba(0, 0, 0, 0.5)
    padding 0.35rem

.mention-item
    width 100%
    display flex
    align-items center
    gap 0.75rem
    padding 0.65rem
    border-radius 8px
    transition background 0.15s

    &:hover
        background #3a3a3a

.mention-item-active
    background rgba(119, 0, 255, 0.35)

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