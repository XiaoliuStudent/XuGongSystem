<template>
  <el-table

      ref="multipleTableRef"
      :data="tableData"
      style="width: 100%"
      @selection-change="handleSelectionChange"
  >
    <el-table-column type="selection" width="55"/>
    <el-table-column property="xuehao" label="学号" width="120"/>
    <el-table-column property="class" label="班级" width="120"/>
    <el-table-column property="name" label="姓名" width="120"/>


    <el-table-column
        prop="clock-status"
        label="是否完成"
        width="100"
        :filters="[
        { text: '已完成', value: '已完成' },
        { text: '未完成', value: '未完成' },
      ]"
        :filter-method="filterTag"
        filter-placement="bottom-start"
    >
      <template #default="scope">
        <el-tag :type="scope.row.clockstatus === '已完成' ? '' : 'success'" disable-transitions>{{
            scope.row.clockstatus
          }}
        </el-tag>
      </template>
    </el-table-column>

    <el-table-column property="comment" label="备注" show-overflow-toolti>
        <a-input v-model:value="comment" placeholder="" style="width: 260px"/>
    </el-table-column>


  </el-table>
  <div style="margin-top: 20px">
    <el-button @click="toggleSelection([tableData[1], tableData[2]])"
    >一键选择未打卡记录
    </el-button
    >
    <el-button @click="toggleSelection()">取消选择</el-button>
  </div>

</template>

<script lang="ts" setup>
import {ref} from 'vue'
import {ElTable} from 'element-plus'

interface User {
  xuehao: string
  class: string
  name: string
  clockstatus: string
}


// TODO: improvement typing when refactor table
const clearFilter = () => {
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-expect-error
  tableRef.value!.clearFilter()
}
const formatter = (row: User, column: TableColumnCtx<User>) => {
  return row.address
}
const filterTag = (value: string, row: User) => {
  return row.clockstatus === value
}
const filterHandler = (
    value: string,
    row: User,
    column: TableColumnCtx<User>
) => {
  const property = column['property']
  return row[property] === value
}

const multipleTableRef = ref<InstanceType<typeof ElTable>>()
const multipleSelection = ref<User[]>([])
const toggleSelection = (rows?: User[]) => {
  if (rows) {
    rows.forEach((row) => {
      // TODO: improvement typing when refactor table
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-expect-error
      multipleTableRef.value!.toggleRowSelection(row, undefined)
    })
  } else {
    multipleTableRef.value!.clearSelection()
  }
}
const handleSelectionChange = (val: User[]) => {
  multipleSelection.value = val
}

const tableData: User[] = [
  {xuehao: '200090102139', class: '20计转本', name: '刘航宇', clockstatus: '已完成'},
  {xuehao: '200090102138', class: '20计转本', name: '刘磊', clockstatus: '未完成'}
]
</script>
