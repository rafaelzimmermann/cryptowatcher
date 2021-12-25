<template>
<div class="container-fluid">
    <div class="row">
      <nav id="sidebarMenu" class="col-md-3 col-lg-3 d-md-block bg-light sidebar collapse">
        <div class="position-sticky pt-1">
          <ul class="nav flex-column">
            <li class="nav-item">
                <router-link class="nav-link active" aria-current="page" to="/">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-home" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
                    Balance
                </router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/import">
                  <i class="bi bi-file-arrow-down"></i>
                    Import
                </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/transactions">
                <i class="bi bi-card-checklist"></i>
                Transactions
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/configuration">
                <i class="bi bi-gear"></i>
                Configuration
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/support">
                <i class="bi bi-heart"></i>
                Support
              </router-link>
            </li>
          </ul>
        </div>
      </nav>
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4" id="app">
        <slot></slot>
      </main>
    </div>
</div>
</template>

<script>
export default {
  name: 'MainContainer',
  data: () => ({
    manual_portifolio: {}
  })
}
</script>

<style>
</style>