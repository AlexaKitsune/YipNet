<template>
    <YipNetLayout :user-data="userData" :on-session="onSession" class="Chat-MAIN">
        <template #sidebar="{ closeSidebar }">
            <MessageListing
                @loaded="setConversationFromList"
                @new-chat="openNewChat(closeSidebar)"
            />
        </template>

        <main class="h-[calc(100vh-80px)] flex flex-col">
            <div v-if="!conversationId" class="flex h-full items-center justify-center opacity-60">
                {{ $t('chat.selectConversation') }}
            </div>

            <template v-else>
                <section class="chat-topbar">
                    <UAvatar :src="conversationAvatar" :alt="conversationTitle" size="sm" />
                    <div class="min-w-0 flex-1">
                        <p class="truncate font-semibold">
                            {{ conversationTitle }}
                        </p>
                        <p class="truncate text-xs opacity-60">
                            {{ conversationSubtitle }}
                        </p>
                    </div>
                    <UDropdownMenu :items="conversationMenuItems" :ui="{ content: 'z-[9999] bg-black border border-white/10' }" variant="ghost">
                        <UButton
                            icon="i-lucide-ellipsis"
                            variant="ghost"
                            color="neutral"
                        />
                    </UDropdownMenu>
                </section>

                <section ref="messagesBox" class="flex-1 overflow-y-auto space-y-3 p-4">
                    <MessageRenderer
                        v-for="message in messages"
                        :key="message.id"
                        :message-data="message"
                        :current-user-id="Number(userData.id)"
                    />
                </section>

                <section class="border-t border-white/10 p-3">
                    <div v-if="filesInput.files.length" class="mb-3 rounded-lg bg-black/20 p-3">
                        <div class="flex gap-2 overflow-x-auto">
                            <div v-for="(item, index) in filesInput.files" :key="index">
                                <img
                                    v-if="item.type.startsWith('image/')"
                                    :src="item.url"
                                    class="size-20 rounded object-cover"
                                >
                                <video
                                    v-else-if="item.type.startsWith('video/')"
                                    class="size-20 rounded object-cover"
                                >
                                    <source :src="item.url + '#t=1'" :type="item.type">
                                </video>
                                <div v-else class="text-sm opacity-70">
                                    {{ item.name }}
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="flex items-end gap-2">
                        <label class="files-input">
                            <UButton icon="i-lucide-paperclip" variant="ghost" color="neutral" />
                            <input
                                type="file"
                                multiple
                                @change="setFilesPreview"
                                ref="chatFilesInput"
                                :disabled="uploading"
                            >
                        </label>

                        <UButton
                            icon="i-lucide-trash-2"
                            variant="ghost"
                            color="neutral"
                            :disabled="uploading || !filesInput.files.length"
                            @click="deleteFiles"
                        />

                        <UTextarea
                            v-model="msgText"
                            autoresize
                            :rows="1"
                            placeholder="Message..."
                            class="flex-1"
                            :disabled="uploading"
                            :ui="{ base: 'bg-black text-white placeholder:text-gray-500 max-h-40' }"
                            @keydown.enter.exact.prevent="sendMessage"
                        />

                        <UButton
                            icon="i-lucide-send"
                            color="primary"
                            :loading="uploading"
                            :disabled="uploading || (!msgText.trim() && !filesInput.files.length)"
                            @click="sendMessage"
                        />
                    </div>
                </section>
            </template>
        </main>
    </YipNetLayout>

    <!-- create new chat -->
    <UModal
        v-model:open="newChatOpen"
        :ui="{ content: 'max-w-[520px] w-[min(92vw,520px)] bg-[var(--alexicon-surface)] text-[var(--alexicon-text)]', overlay: 'bg-black/60 backdrop-blur-sm' }"
    >
        <template #content>
            <UCard class="bg-[var(--alexicon-surface)] border-0" variant="ghost">
                <template #header>
                    <div class="flex items-center justify-between">
                        <h2 class="text-lg font-bold">{{ $t('chat.newChat') }}</h2>

                        <UButton
                            icon="i-lucide-x"
                            variant="ghost"
                            color="neutral"
                            @click="newChatOpen = false"
                        />
                    </div>
                </template>

                <div class="space-y-4 create-new-chat">
                    <UInput
                        v-model="newChatQuery"
                        icon="i-lucide-search"
                        :placeholder="$t('chat.placeholderSearchUsers')"
                        variant="none"
                        class="w-full new-chat-input"
                        :ui="{
                            base: 'bg-black rounded-md',
                            input: 'text-white placeholder:text-gray-500'
                        }"
                        @keyup.enter="searchUsersForChat"
                    />

                    <div v-if="selectedUsers.length > 1" class="space-y-1">
                        <p class="text-xs uppercase tracking-widest opacity-50">
                            {{ $t('chat.groupName') }}
                        </p>

                        <UInput
                            v-model="newChatName"
                            :placeholder="$t('chat.placeholderNewGroup')"
                            variant="none"
                            class="new-chat-input w-full"
                            :ui="{
                                base: 'bg-black rounded-md',
                                input: 'text-white placeholder:text-gray-500'
                            }"
                        />
                    </div>

                    <div v-if="selectedUsers.length" class="flex flex-wrap gap-2">
                        <UBadge
                            v-for="user in selectedUsers"
                            :key="user.id"
                            color="primary"
                            variant="soft"
                            class="cursor-pointer"
                            @click="toggleSelectedUser(user)"
                        >
                            {{ user.name }} {{ user.surname }} ✕
                        </UBadge>
                    </div>

                    <div class="max-h-72 overflow-y-auto space-y-2">
                        <button
                            v-for="user in newChatUsers"
                            :key="user.id"
                            class="chat-user-result"
                            :class="{ 'chat-user-result-active': isUserSelected(user.id) }"
                            @click="toggleSelectedUser(user)"
                        >
                            <UAvatar :src="userAvatar(user.profile_pic)" />

                            <div class="min-w-0 text-left">
                                <p class="truncate font-semibold">
                                    {{ user.name }} {{ user.surname }}
                                </p>
                                <p class="truncate text-xs opacity-60">
                                    @{{ user.at_sign || user.nickname }}
                                </p>
                            </div>

                            <UIcon v-if="isUserSelected(user.id)" name="i-lucide-check" class="ml-auto text-[#7700ff]"/>
                        </button>
                    </div>

                    <p v-if="newChatQuery && !newChatUsers.length" class="text-sm opacity-60">
                        {{ $t('chat.noUsersFound') }}
                    </p>
                </div>

                <template #footer>
                    <div class="flex justify-end gap-2">
                        <UButton color="neutral" variant="ghost" @click="resetNewChat">
                            {{ $t('chat.cancelBtn') }}
                        </UButton>
                        <UButton color="primary" :loading="creatingChat" :disabled="!selectedUsers.length" @click="createNewChat">
                            {{ selectedUsers.length > 1 ? $t('chat.createGroup') : $t('chat.createChat') }}
                        </UButton>
                    </div>
                </template>
            </UCard>
        </template>
    </UModal>

    <!-- edit data chat -->
    <UModal v-model:open="editGroupNameOpen" :ui="{ content: 'max-w-[520px] w-[min(92vw,520px)] bg-[var(--alexicon-surface)] text-[var(--alexicon-text)]', overlay: 'bg-black/60 backdrop-blur-sm' }">
        <template #content>
            <UCard class="bg-[var(--alexicon-surface)] border-0" variant="ghost">
                <template #header>
                    <h2 class="font-bold">{{ $t('chat.editGroupName') }}</h2>
                </template>

                <UInput
                    v-model="editGroupNameValue"
                    placeholder="Group name"
                    variant="none"
                    class="new-chat-input w-full"
                    :ui="{ base: 'bg-black rounded-md' }"
                />

                <template #footer>
                    <div class="flex justify-end gap-2">
                        <UButton variant="ghost" color="neutral" @click="editGroupNameOpen = false">
                            {{ $t('chat.cancelBtn') }}
                        </UButton>
                        <UButton color="primary" :loading="savingGroupName" @click="saveGroupName">
                            {{ $t('chat.saveBtn') }}
                        </UButton>
                    </div>
                </template>
            </UCard>
        </template>
    </UModal>

    <!-- manage members -->
    <UModal
        v-model:open="manageMembersOpen"
        :ui="{ content: 'max-w-[560px] w-[min(92vw,560px)] bg-[var(--alexicon-surface)] text-[var(--alexicon-text)]', overlay: 'bg-black/60 backdrop-blur-sm' }"
    >
        <template #content>
            <UCard class="bg-[var(--alexicon-surface)] border-0" variant="ghost">
                <template #header>
                    <div class="flex items-center justify-between">
                        <h2 class="font-bold">{{ canManageCurrentConversation ? 'Manage members' : 'Members' }}</h2>
                        <UButton icon="i-lucide-x" variant="ghost" color="neutral" @click="manageMembersOpen = false" />
                    </div>
                </template>

                <div class="space-y-2">
                    <div
                        v-for="member in currentConversation?.participants || []"
                        :key="member.id"
                        class="flex items-center gap-3 rounded-lg bg-black/20 p-3"
                    >
                        <UAvatar :src="userAvatar(member.profile_pic)" />

                        <div class="min-w-0 flex-1">
                            <p class="truncate font-semibold">
                                {{ member.name }} {{ member.surname }}
                            </p>

                            <div class="flex items-center gap-2 text-xs opacity-60">
                                <span>@{{ member.at_sign || member.nickname }}</span>

                                <UBadge
                                    size="xs"
                                    color="neutral"
                                    variant="soft"
                                >
                                    {{ member.role }}
                                </UBadge>
                            </div>
                        </div>

                        <div
                            v-if="canManageCurrentConversation && Number(member.id) !== Number(userData.id)"
                            class="flex items-center gap-1"
                        >
                            <UDropdownMenu :items="memberMenuItems(member)">
                                <UButton
                                    icon="i-lucide-ellipsis"
                                    color="neutral"
                                    variant="ghost"
                                />
                            </UDropdownMenu>
                        </div>
                    </div>
                </div>
            </UCard>
        </template>
    </UModal>

    <ConfirmDialog
        v-model:open="confirmOpen"
        :title="confirmTitle"
        :description="confirmDescription"
        :confirm-label="confirmLabel"
        confirm-color="error"
        :loading="confirmLoading"
        @confirm="runConfirmAction"
    />
</template>

<script>
const API_URL = import.meta.env.VITE_API_URL
import YipNetLayout from '@/layouts/YipNetLayout.vue'
import MessageListing from '@/components/MessageListing.vue'
import MessageRenderer from '@/components/MessageRenderer.vue'
import {
    getConversationMessages,
    sendConversationMessage,
    createConversation,
    getOrCreateDirectConversation,
    updateConversation,
    leaveConversation,
    addConversationParticipants,
    removeConversationParticipant,
    updateConversationParticipantRole
} from '@/services/yipnet/messages'
import { searchGlobal } from '@/services/yipnet/search'
import { uploadFile } from '@/services/alexicon/media'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

export default {
    name: 'Chat',
    components: {
        YipNetLayout,
        MessageListing,
        MessageRenderer,
        ConfirmDialog,
    },
    props: {
        userData: {
            type: Object,
            default: () => ({})
        },
        onSession: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            messages: [],
            msgText: '',
            uploading: false,
            uploadedFilesArray: [],
            filesInput: {
                files: []
            },
            currentConversation: null,
            // new chat
            newChatOpen: false,
            newChatQuery: '',
            newChatUsers: [],
            selectedUsers: [],
            newChatName: '',
            creatingChat: false,

            editGroupNameOpen: false,
            editGroupNameValue: '',
            savingGroupName: false,
            manageMembersOpen: false,

            conversations: [],
            currentConversation: null,

            confirmOpen: false,
            confirmTitle: '',
            confirmDescription: '',
            confirmLabel: 'Confirm',
            confirmLoading: false,
            confirmAction: null,
        }
    },
    computed: {
        conversationId() {
            return Number(this.$route.params.id) || null
        },

        conversationTitle() {
            return this.currentConversation?.display_name ||
                this.currentConversation?.name ||
                'Conversation'
        },

        conversationSubtitle() {
            if (!this.currentConversation) return ''
            if (this.currentConversation.is_group)
                return `${this.currentConversation.participants?.length || 0} members`
            return 'Direct message'
        },

        conversationAvatar() {
            const pic = this.currentConversation?.display_pic
            if (!pic) return '';
            if (String(pic).startsWith('/'))
                return `${API_URL}${pic}`;
            return `${API_URL}/alexicon/media/${pic}`;
        },

        myConversationRole() {
            const myId = Number(this.userData.id);
            return this.currentConversation?.participants?.find(
                user => Number(user.id) === myId
            )?.role || null
        },

        isGroupChat() {
            return !!this.currentConversation?.is_group
        },

        canManageCurrentConversation() {
            return ['owner', 'admin'].includes(this.myConversationRole)
        },

        conversationMenuItems() {
            const items = [
                [
                    {
                        label: 'Find in chat',
                        icon: 'i-lucide-search',
                        onSelect: () => this.openBrowserFind()
                    }
                ]
            ]

            if (this.isGroupChat) {
                const groupItems = [];

                groupItems.push({
                    label: this.canManageCurrentConversation ? 'Manage members' : 'View members',
                    icon: 'i-lucide-users',
                    onSelect: () => this.openManageMembers()
                });

                if (this.canManageCurrentConversation) {
                    groupItems.push({
                        label: 'Edit group name',
                        icon: 'i-lucide-pencil',
                        onSelect: () => this.openEditGroupName()
                    });
                }

                groupItems.push({
                    label: 'Leave chat',
                    icon: 'i-lucide-log-out',
                    color: 'error',
                    onSelect: () => this.leaveCurrentChat()
                });

                items.push(groupItems);
            }

            return items;
        },
    },
    methods: {
        async loadMessages() {
            if (!this.conversationId) return

            const result = await getConversationMessages(this.conversationId)
            this.messages = result.data?.messages || []

            this.$nextTick(this.scrollBottom)
        },

        setConversationFromList(conversations) {
            this.conversations = conversations || []
            this.syncCurrentConversation()
        },

        syncCurrentConversation() {
            this.currentConversation = this.conversations.find(
                item => Number(item.id) === Number(this.conversationId)
            ) || null
        },

        scrollBottom() {
            const el = this.$refs.messagesBox
            if (el) el.scrollTop = el.scrollHeight
        },

        setFilesPreview(event) {
            for (const file of event.target.files) {
                const isMedia = file.type.startsWith('image/') || file.type.startsWith('video/')

                this.filesInput.files.push({
                    file,
                    url: isMedia ? URL.createObjectURL(file) : null,
                    type: file.type,
                    isMedia,
                    name: file.name
                })
            }
        },

        deleteFiles() {
            for (const item of this.filesInput.files) {
                if (item.url) URL.revokeObjectURL(item.url)
            }

            this.filesInput.files = []

            if (this.$refs.chatFilesInput) {
                this.$refs.chatFilesInput.value = ''
            }
        },

        async sendMessage() {
            if (this.uploading) return
            if (!this.conversationId) return
            if (!this.msgText.trim() && !this.filesInput.files.length) return

            this.uploading = true
            this.uploadedFilesArray = []

            try {
                const files = this.filesInput.files.map(item => item.file)

                if (files.length) {
                    const userId = localStorage.getItem('alexicon_user_id')
                    const targetPath = `yipnet/${userId}/messages/`

                    const results = await Promise.all(
                        files.map(file => uploadFile(file, {
                            targetPath,
                            visibility: 'public'
                        }))
                    )

                    this.uploadedFilesArray = results
                        .map(item => item.data?.fileId || item.fileId || item.data?.id || item.id)
                        .filter(Boolean)
                }

                await sendConversationMessage(this.conversationId, {
                    content: this.msgText,
                    media: this.uploadedFilesArray
                })

                this.msgText = ''
                this.deleteFiles()
                await this.loadMessages()
            } finally {
                this.uploading = false
            }
        },

        userAvatar(value) {
            if (!value) return ''
            if (String(value).startsWith('/')) 
                return `${API_URL}${value}`
            return `${API_URL}/alexicon/media/${value}`
        },

        async searchUsersForChat() {
            const q = this.newChatQuery.trim()

            if (!q) {
                this.newChatUsers = []
                return
            }

            const result = await searchGlobal({
                q,
                type: 'users',
                from: '',
                to: ''
            })

            const myId = Number(localStorage.getItem('alexicon_user_id'))

            this.newChatUsers = (result.data?.users || [])
                .filter(user => Number(user.id) !== myId)
        },

        isUserSelected(userId) {
            return this.selectedUsers.some(user => Number(user.id) === Number(userId))
        },

        toggleSelectedUser(user) {
            if (this.isUserSelected(user.id)) {
                this.selectedUsers = this.selectedUsers.filter(
                    item => Number(item.id) !== Number(user.id)
                )
                return
            }

            this.selectedUsers.push(user)
        },

        async createNewChat() {
            if (!this.selectedUsers.length) return

            if (this.selectedUsers.length > 1 && !this.newChatName.trim()) {
                this.newChatName = 'New group'
            }

            this.creatingChat = true

            try {
                let conversationId = null

                if (this.selectedUsers.length === 1) {
                    const result = await getOrCreateDirectConversation(this.selectedUsers[0].id)
                    conversationId = result.data?.conversation_id
                } else {
                    const result = await createConversation({
                        name: this.newChatName.trim(),
                        participants: this.selectedUsers.map(user => user.id),
                        current_group_pic: null
                    })

                    conversationId = result.data?.conversation_id
                }

                this.resetNewChat()

                if (conversationId) {
                    this.$router.push(`/chat/${conversationId}`)
                }
            } finally {
                this.creatingChat = false
            }
        },

        resetNewChat() {
            this.newChatOpen = false
            this.newChatQuery = ''
            this.newChatUsers = []
            this.selectedUsers = []
            this.newChatName = ''
        },

        openBrowserFind() {
            document.dispatchEvent(
                new KeyboardEvent('keydown', {
                    key: 'f',
                    code: 'KeyF',
                    metaKey: navigator.platform.toLowerCase().includes('mac'),
                    ctrlKey: !navigator.platform.toLowerCase().includes('mac'),
                    bubbles: true
                })
            )
        },

        openEditGroupName() {
            this.editGroupNameValue = this.currentConversation?.name || '';
            this.editGroupNameOpen = true;
        },

        openManageMembers() {
            this.manageMembersOpen = true;
        },

        leaveCurrentChat() {
            this.openConfirm({
                title: 'Leave this chat?',
                description: 'You will no longer see this conversation in your chat list.',
                confirmLabel: 'Leave',
                action: async () => {
                    await leaveConversation(this.conversationId)
                    this.$router.push('/chat')
                }
            })
        },

        async saveGroupName() {
            if (!this.editGroupNameValue.trim()) return

            this.savingGroupName = true

            try {
                await updateConversation(this.conversationId, {
                    name: this.editGroupNameValue.trim()
                })

                if (this.currentConversation) {
                    this.currentConversation.name = this.editGroupNameValue.trim()
                    this.currentConversation.display_name = this.editGroupNameValue.trim()
                }

                this.syncCurrentConversation()
                this.editGroupNameOpen = false
            } finally {
                this.savingGroupName = false
            }
        },

        removeMember(member) {
            this.openConfirm({
                title: `Remove ${member.name} from this chat?`,
                description: 'This user will be removed from the conversation.',
                confirmLabel: 'Remove',
                action: async () => {
                    await removeConversationParticipant(this.conversationId, member.id)

                    if (this.currentConversation?.participants) {
                        this.currentConversation.participants =
                            this.currentConversation.participants.filter(
                                item => Number(item.id) !== Number(member.id)
                            )
                    }
                }
            })
        },

        memberMenuItems(member) {
            const items = [];

            if (this.myConversationRole === 'owner') {
                items.push([
                    {
                        label: 'Make member',
                        icon: 'i-lucide-user',
                        disabled: member.role === 'member',
                        onSelect: () => this.changeMemberRole(member, 'member')
                    },
                    {
                        label: 'Make admin',
                        icon: 'i-lucide-shield',
                        disabled: member.role === 'admin',
                        onSelect: () => this.changeMemberRole(member, 'admin')
                    },
                    {
                        label: 'Make owner',
                        icon: 'i-lucide-crown',
                        disabled: member.role === 'owner',
                        onSelect: () => this.changeMemberRole(member, 'owner')
                    }
                ]);
            }

            items.push([
                {
                    label: 'Remove from chat',
                    icon: 'i-lucide-user-minus',
                    color: 'error',
                    onSelect: () => this.removeMember(member)
                }
            ]);

            return items;
        },

        async changeMemberRole(member, role) {
            await updateConversationParticipantRole(this.conversationId, member.id, role);

            member.role = role;
        },

        openConfirm({ title, description = '', confirmLabel = 'Confirm', action }) {
            this.confirmTitle = title
            this.confirmDescription = description
            this.confirmLabel = confirmLabel
            this.confirmAction = action
            this.confirmOpen = true
        },

        async runConfirmAction() {
            if (!this.confirmAction) return

            this.confirmLoading = true

            try {
                await this.confirmAction()
                this.confirmOpen = false
                this.confirmAction = null
            } finally {
                this.confirmLoading = false
            }
        },

        openNewChat(closeSidebar) {
            if (typeof closeSidebar === 'function') {
                closeSidebar()
            }
            this.newChatOpen = true
        }
    },
    async mounted() {
        this.loadMessages();
        await this.$nextTick();
        document.getElementById("main-sidebar-btn")?.click();
    },
    watch: {
        conversationId() {
            this.syncCurrentConversation()
            this.loadMessages()
        }
    },
    beforeUnmount() {
        this.deleteFiles()
    }
}
</script>

<style scoped lang="stylus">
.chat-topbar
    position sticky
    top 0
    display flex
    align-items center
    gap 0.75rem
    padding 0.75rem 1rem
    background var(--alexicon-surface)
    border-bottom 1px solid rgba(255, 255, 255, 0.08)
    box-shadow 0 0 1ch rgba(0, 0, 0, 0.25)
    border-radius: 0 0 20px 20px

.files-input
    position relative
    display inline-block

    input[type="file"]
        position absolute
        inset 0
        width 100%
        height 100%
        opacity 0
        cursor pointer

.chat-user-result
    width 100%
    display flex
    align-items center
    gap 0.75rem
    padding 0.75rem
    border-radius 10px
    background rgba(0, 0, 0, 0.18)
    transition all 0.15s

    &:hover
        background #3a3a3a

.chat-user-result-active
    background rgba(119, 0, 255, 0.18)

.new-chat-input:deep(input)
    color white !important

.new-chat-input:deep(input::placeholder)
    color #6b7280 !important
</style>