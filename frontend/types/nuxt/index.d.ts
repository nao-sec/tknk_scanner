import { NuxtAxiosInstance } from "@nuxtjs/axios"
import { accessorType } from "~/store"

export interface Context {
  $axios: NuxtAxiosInstance
}

declare module "vue/types/vue" {
  interface Vue {
    $accessor: typeof accessorType
  }
}

declare module "@nuxt/types" {
  interface NuxtAppOptions {
    $accessor: typeof accessorType
  }
}
