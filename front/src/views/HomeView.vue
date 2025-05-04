<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Définir une variable réactive pour stocker les données
const documents = ref([])
const error = ref(null)
const differences = ref([])

// Fonction pour récupérer les documents depuis l'API Flask
const fetchDocuments = async () => {
  try {
    const response = await axios.get('http://localhost:7003/all') // Remplacez par l'URL de votre API
    documents.value = response.data.data
    differences.value = compareData(documents)
  } catch (err) {
    error.value = 'Erreur lors de la récupération des documents : ' + err.message
  }
}
onMounted(() => {
  fetchDocuments()
})
// Function to compare old and new data
const compareData = (documents) => {
  let differences = []
  for(const document of documents.value) {
  differences.push({
    name: document.old.name !== document.new.name ? { old: document.old.name, new: document.new.name } : document.old.name,
    number_of_employees: document.old.number_of_employees !== document.new.number_of_employees
      ? { old: document.old.number_of_employees, new: document.new.number_of_employees }
      : document.old.number_of_employees,
    is_serious: document.old.is_serious !== document.new.is_serious
      ? { old: document.old.is_serious ? "Yes" : "No", new: document.new.is_serious ? "Yes" : "No" }
      : document.old.is_serious,
    tags: document.old.tags.toString() !== document.new.tags.toString()
      ? { old: document.old.tags, new: Array.from(new Set([...document.old.tags, ...document.new.tags])) }
      : document.old.tags
  })
}
  return differences
}
</script>

<template>
  <div>
    <h1>Comparison of Old and New Data</h1>
    <div v-for="(difference, index) in differences" :key="index">
      <h2>Document {{ index + 1 }}</h2>
      <ul>
      <!-- Name -->
      <li v-if="difference.name.old">
        <span>Name : </span>
        <span class="strikethrough">{{ difference.name.old }}</span>
        <span class="bold">{{ difference.name.new }}</span>
      </li>
      <li v-else>
        <span>Name : </span>
        <span class="bold">{{ difference.name }}</span>
      </li>
      <li v-if="difference.number_of_employees.old">
        <span>Number of Employees : </span>
        <span class="strikethrough">{{ difference.number_of_employees.old }}</span>
        <span class="bold">{{ difference.number_of_employees.new }}</span>
      </li>
      <li v-else>
        <span>Number of Employees : </span>
        <span>{{ difference.number_of_employees }}</span>
      </li>
      <li v-if="difference.is_serious.old">
        <span>Is Serious : </span>
        <span class="strikethrough">{{ difference.is_serious.old }}</span>
        <span class="bold">{{ difference.is_serious.new }}</span>
      </li>
      <li v-else>
        <span>Is Serious : </span>
        <span>{{ difference.is_serious }}</span>
      </li>

      <!-- Tags -->
      <li v-if="difference.tags">
        <span>Tags : </span>
        <span class="strikethrough">{{ difference.tags.old.join(", ") }}</span>
        <span class="bold">{{ difference.tags.new.join(", ") }}</span>
      </li>
      <li v-else>
        <span>Tags : </span>
        <span>{{ difference.tags.join(", ") }}</span>
      </li>
    </ul>
    </div>
  </div>
</template>

<style>
.strikethrough {
  text-decoration: line-through;
  color: red;
}
.error {
  color: red;
  font-weight: bold;
}
.bold {
  font-weight: bold;
  color: green;
}
</style>