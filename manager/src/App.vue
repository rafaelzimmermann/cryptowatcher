<template>
  <div>
    <Header></Header>
    <MainContainer>
      <router-view/>
    </MainContainer>
  </div>
</template>

<script>
import Header from './components/Header.vue'
import MainContainer from './components/MainContainer.vue'

export default {
  name: 'App',
  components: {
    Header,
    MainContainer
  }
}
</script>

<style>

</style>
