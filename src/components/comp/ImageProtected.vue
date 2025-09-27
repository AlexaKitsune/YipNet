<template>
	<img v-if="asyncSrc" :src="asyncSrc" :key="keyUpdater">
</template>

<script>
export default {
	name: 'ImageProtected',
	props: {
		mediaId: { type: [Number, String], default: null },
	},
	data() {
		return {
			asyncSrc: '',
			keyUpdater: 0,
			retryTimer: null,
		};
	},
	computed: {
		isValidId() {
			const n = Number(this.mediaId);
			return Number.isFinite(n) && n > 0;
		}
	},
	watch: {
		mediaId: {
			immediate: true,
			handler() {
				this.clearBlob();
				if (this.isValidId) this.fetchWithRetry(Number(this.mediaId));
			}
		}
	},
	methods: {
		clearBlob() {
			if (this.asyncSrc && this.asyncSrc.startsWith('blob:')) {
				URL.revokeObjectURL(this.asyncSrc);
			}
			this.asyncSrc = '';
		},

		scheduleRetry(fn, attempt) {
			const delay = 300 * attempt; // 300, 600, 900, 1200, 1500 ms
			this.retryTimer = setTimeout(fn, Math.min(delay, 1500));
		},

		async fetchWithRetry(id, attempt = 1, maxAttempts = 5) {
			const ok = await this.loadOnce(id);
			if (ok) return;

			if (attempt < maxAttempts) {
				this.scheduleRetry(() => this.fetchWithRetry(id, attempt + 1, maxAttempts), attempt);
			} else {
				// podrías emitir un evento para avisar al padre
				// this.$emit('media-failed', { id });
				// console.warn(`Media ${id} no se pudo cargar tras ${maxAttempts} intentos`);
			}
		},

		async loadOnce(id) {
			const base = this.$ENDPOINT;
			const url = `${base}/alexicon/media/file/${id}`;

			// 1) intento público
			try {
				const r = await fetch(url, { cache: 'no-store' });
				if (r.ok) {
					this.asyncSrc = url;
					this.keyUpdater++;
					return true;
				}
				if (r.status !== 401 && r.status !== 403) {
					// 404/500 → probablemente aún no listo; que el retry decida
					return false;
				}
			} catch (_) {
				// error de red → reintenta
			}

			// 2) requiere token
			let token = localStorage.getItem('AlexiconUserToken');
			if (!token) {
				//token = prompt('Este recurso requiere autenticación.\nPega tu token (JWT):', '') || '';
				if (!token) return false;
				localStorage.setItem('AlexiconUserToken', token);
			}

			try {
				const r2 = await fetch(url, {
					headers: { Authorization: `Bearer ${token}` },
					cache: 'no-store',
				});
				if (!r2.ok) return false;

				const blob = await r2.blob();
				const blobUrl = URL.createObjectURL(blob);

				this.clearBlob();
				this.asyncSrc = blobUrl;
				this.keyUpdater++;
				return true;
			} catch {
				return false;
			}
		}
	},
	beforeUnmount() {
		if (this.retryTimer) clearTimeout(this.retryTimer);
		this.clearBlob();
	}
};
</script>
