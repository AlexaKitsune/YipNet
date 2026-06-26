<template>
    <YipNetLayout :user-data="userData" :on-session="onSession" class="Settings-MAIN">
        <br/>
        <h1></h1>
        
        <main class="mx-auto max-w-[760px] space-y-6">
            <h1 class="text-2xl font-bold">{{ $t('settings.title') }}</h1>

            <div class="settings-toast">
                <UAlert
                    v-if="message"
                    color="success"
                    variant="soft"
                    :title="message"
                />

                <UAlert
                    v-if="errorMessage"
                    color="error"
                    variant="soft"
                    icon="i-lucide-triangle-alert"
                    :title="errorMessage"
                />
            </div>

            <!-- profile -->
            <UCard class="bg-black/20 border-0" variant="ghost">
                <template #header>
                    <h2 class="font-semibold">{{ $t('settings.profileInfo') }}</h2>
                    <p class="text-sm opacity-60">{{ $t('settings.profileInfoDescription') }}</p>
                </template>

                <div class="grid gap-3 md:grid-cols-2">
                    <UInput v-model="profileForm.name" :placeholder="$t('settings.placeholderName')" />
                    <UInput v-model="profileForm.surname" :placeholder="$t('settings.placeholderSurname')" />
                    <UInput v-model="profileForm.nickname" placeholder="Nickname" />
                    <UInput v-model="profileForm.at_sign" placeholder="@ username" />
                    <UInput v-model="profileForm.birthday" type="date" />
                    <USelect
                        v-model="profileForm.gender"
                        :items="[
                            { label: 'Woman', value: 'woman' },
                            { label: 'Man', value: 'man' },
                            { label: 'Non-binary', value: 'non_binary' },
                            { label: 'Other', value: 'other' }
                        ]"
                    />
                </div>

				<br/>
                <div class="md:col-span-2">
					<UTextarea
						v-model="profileForm.description"
						autoresize
						:rows="4"
						class="w-full"
						:ui="{
							base: 'w-full min-h-[120px] bg-black text-white'
						}"
                        :placeholder="$t('settings.placeholderDescription')"
					/>
				</div>

                <div class="mt-4 flex justify-end">
                    <UButton
                        color="primary"
                        :loading="savingProfile"
                        @click="saveProfile"
                    >
                        {{ $t('settings.saveProfile') }}
                    </UButton>
                </div>
            </UCard>

            <!-- preferences -->
            <UCard class="bg-black/20 border-0" variant="ghost">
                <template #header>
                    <h2 class="font-semibold">{{ $t('settings.preferences') }}</h2>
                    <p class="text-sm opacity-60">{{ $t('settings.preferencesDescription') }}</p>
                </template>

                <div class="space-y-3">
                    <label class="setting-row">
                        <div>
                            <p class="font-semibold">{{ $t('settings.showNSFW') }}</p>
                            <p class="text-sm opacity-60">{{ $t('settings.showNSFWDescription') }}</p>
                        </div>
                        <USwitch v-model="settingsForm.show_nsfw" />
                    </label>

                    <label class="setting-row">
                        <div>
                            <p class="font-semibold">{{ $t('settings.hideDeadname') }}</p>
                            <p class="text-sm opacity-60">{{ $t('settings.hideDeadnameDescription') }}</p>
                        </div>
                        <USwitch v-model="settingsForm.hide_deadname" />
                    </label>

                    <label class="setting-row">
                        <div>
                            <p class="font-semibold">{{ $t('settings.replaceDeadname') }}</p>
                            <p class="text-sm opacity-60">{{ $t('settings.replaceDeadnameDescription') }}</p>
                        </div>
                        <USwitch v-model="settingsForm.replace_deadname" />
                    </label>

                    <div class="grid gap-3 md:grid-cols-2">
                        <UInput v-model="settingsForm.deadname" :placeholder="$t('settings.placeholderDeadname')" />
                        <UInput v-model="settingsForm.chosen_name" :placeholder="$t('settings.placeholderChosenName')" />
                    </div>

                    <USelect
                        v-model="settingsForm.language"
                        :items="[
                            { label: 'English', value: 'en' },
                            { label: 'Español', value: 'es' },
                            { label: '日本語', value: 'ja' },
                        ]"
                        placeholder="Language"
                    />
                </div>

                <div class="mt-4 flex justify-end">
                    <UButton
                        color="primary"
                        :loading="savingSettings"
                        @click="saveSettings"
                    >
                        {{ $t('settings.savePreferences') }}
                    </UButton>
                </div>
            </UCard>

            <!-- password -->
            <UCard class="bg-black/20 border-0" variant="ghost">
                <template #header>
                    <h2 class="font-semibold">{{ $t('settings.password') }}</h2>
                    <p class="text-sm opacity-60">{{ $t('settings.passwordDescription') }}</p>
                </template>

                <div class="grid gap-3 md:grid-cols-2">
					<UInput
						v-model="passwordForm.current_password"
						type="password"
						:placeholder="$t('settings.placeholderCurrentPassword')"
					/>
					<div></div>
					<UInput
						v-model="passwordForm.new_password"
						type="password"
						:placeholder="$t('settings.placeholderNewPassword')"
					/>
					<UInput
						v-model="passwordForm.confirm_password"
						type="password"
						:placeholder="$t('settings.placeholderConfirmNewPassword')"
					/>
				</div>

                <div class="mt-4 flex justify-end">
                    <UButton
                        color="primary"
                        :loading="savingPassword"
                        @click="savePassword"
                    >
                        {{ $t('settings.changePassword') }}
                    </UButton>
                </div>
            </UCard>

            <!-- blocked -->
             <UCard class="bg-black/20 border-0" variant="ghost">
                <template #header>
                    <h2 class="font-semibold">{{ $t('settings.blockedUsers') }}</h2>
                    <p class="text-sm opacity-60">{{ $t('settings.blockUsersDescription') }}</p>
                </template>

                <div v-if="blockedUsers.length" class="space-y-2">
                    <div
                        v-for="user in blockedUsers"
                        :key="user.id"
                        class="blocked-user-row"
                    >
                        <div class="flex items-center gap-3">
                            <UAvatar :src="userAvatar(user.profile_pic)" />

                            <div>
                                <p class="font-semibold">
                                    {{ user.name }} {{ user.surname }}
                                </p>
                                <p class="text-xs opacity-60">
                                    @{{ user.at_sign || user.nickname }}
                                </p>
                            </div>
                        </div>

                        <UButton
                            color="error"
                            variant="soft"
                            size="sm"
                            @click="unblockFromSettings(user.id)"
                        >
                            {{ $t('settings.unblock') }}
                        </UButton>
                    </div>
                </div>

                <p v-else class="text-sm opacity-60">
                    {{ $t('settings.noBlockedUsers') }}
                </p>
            </UCard>

            <!--<SubscriptionPill />-->

			<br/>
        </main>
    </YipNetLayout>
</template>

<script>
import YipNetLayout from '@/layouts/YipNetLayout.vue'
import SubscriptionPill from '@/components/SubscriptionPill.vue'
import { me, updateProfile, updatePassword } from '@/services/alexicon/users'
import { getSettings, updateSettings } from '@/services/alexicon/settings'
import { getBlockedUsers, unblockUser } from '@/services/alexicon/social'

export default {
    name: 'Settings',
    components: {
        YipNetLayout, SubscriptionPill,
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
            message: '',
            errorMessage: '',

            savingProfile: false,
            savingSettings: false,
            savingPassword: false,
            profileForm: {
                name: '',
                surname: '',
                nickname: '',
                at_sign: '',
                birthday: '',
                gender: '',
                description: ''
            },
            settingsForm: {
                show_nsfw: false,
                hide_deadname: false,
                replace_deadname: false,
                deadname: '',
                chosen_name: '',
                language: 'en'
            },
            passwordForm: {
                current_password: '',
                new_password: '',
                confirm_password: ''
            },
            blockedUsers: [],
        }
    },
    methods: {
        clearMessages() {
            this.message = ''
            this.errorMessage = ''
        },

        async loadData() {
            const [userResult, settingsResult] = await Promise.all([
                me(),
                getSettings()
            ])

            const blockedResult = await getBlockedUsers()
            this.blockedUsers = blockedResult.data?.users || []

            const user = userResult.data || {}
            const settings = settingsResult.data || {}

            this.profileForm = {
                name: user.name || '',
                surname: user.surname || '',
                nickname: user.nickname || '',
                at_sign: user.at_sign || '',
                birthday: user.birthday ? String(user.birthday).slice(0, 10) : '',
                gender: user.gender || '',
                description: user.description || ''
            }

            this.settingsForm = {
                show_nsfw: !!settings.show_nsfw,
                hide_deadname: !!settings.hide_deadname,
                replace_deadname: !!settings.replace_deadname,
                deadname: settings.deadname || '',
                chosen_name: settings.chosen_name || '',
                language: settings.language || 'en'
            }
        },

        async saveProfile() {
            this.clearMessages()
            this.savingProfile = true

            try {
                await updateProfile(this.profileForm)
                this.message = 'Profile updated.'
            } catch (error) {
                this.errorMessage = error.message || 'Could not update profile.'
            } finally {
                this.savingProfile = false
            }
        },

        async saveSettings() {
            this.clearMessages()
            this.savingSettings = true
            this.$i18n.locale = this.settingsForm.language

            try {
                await updateSettings(this.settingsForm)
                this.showMessage('Preferences updated.')
            } catch (error) {
                this.showError(error.message || 'Could not update preferences.')
            } finally {
                this.savingSettings = false
            }
        },

        async savePassword() {
            this.clearMessages()

            if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
                this.errorMessage = 'Passwords do not match.'
                return
            }

            this.savingPassword = true

            try {
                await updatePassword({
                    current_password: this.passwordForm.current_password,
                    new_password: this.passwordForm.new_password
                })

                this.passwordForm = {
                    current_password: '',
                    new_password: '',
                    confirm_password: ''
                }

                this.message = 'Password updated.'
            } catch (error) {
                this.errorMessage = error.message || 'Could not update password.'
            } finally {
                this.savingPassword = false
            }
        },

        showMessage(text) {
            this.message = text
            this.errorMessage = ''

            setTimeout(() => {
                this.message = ''
            }, 3500)
        },

        showError(text) {
            this.errorMessage = text
            this.message = ''

            setTimeout(() => {
                this.errorMessage = ''
            }, 4500)
        },

        userAvatar(value) {
            if (!value) return ''
            if (String(value).startsWith('/')) {
                return `${import.meta.env.VITE_API_URL}${value}`
            }
            return `${import.meta.env.VITE_API_URL}/alexicon/media/${value}`
        },

        async unblockFromSettings(userId) {
            await unblockUser(userId)
            this.blockedUsers = this.blockedUsers.filter(
                user => Number(user.id) !== Number(userId)
            )
            this.showMessage('User unblocked.')
        },
    },

    mounted() {
        this.loadData()
    }
}
</script>

<style scoped lang="stylus">
.setting-row
    display flex
    align-items center
    justify-content space-between
    gap 1rem
    padding 1rem
    border-radius 10px
    background rgba(0, 0, 0, 0.18)

.settings-toast
    position fixed
    top 56px
    right 1rem
    width 420px
    max-width calc(100vw - 2rem)
    z-index 9999
    display flex
    flex-direction column
    gap 0.75rem

.blocked-user-row
    display flex
    align-items center
    justify-content space-between
    gap 1rem
    padding 1rem
    border-radius 10px
    background rgba(0, 0, 0, 0.18)
</style>