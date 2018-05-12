import { createLocalVue, mount } from '@vue/test-utils'

import Tags from '@/components/Admin/Tags'
import TableFilter from '@/components/scaffolding/TableFilter'
import Router from 'vue-router'
import { routes } from '@/router'

const tagListSpy = jest.spyOn(TableFilter.methods, 'clearSelection')

describe('Tags.vue', () => {
  let localVue
  let wrapper

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})

    wrapper = mount(Tags, {
      localVue,
      router
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('If no tags are selected, filter table has full-width', () => {
    expect(wrapper.find('#tag-list').classes()).toContain('col-12')
  })

  it('If one or more tags are selected, filter table has reduced with', () => {
    wrapper.vm.selectedTags = ['asd', 'dsa', 'wasa']
    expect(wrapper.find('#tag-list').classes()).toContain('col-8')
  })

  it('when selection is cleared, table widths comes back to normal', () => {
    wrapper.vm.selectedTags = ['asd', 'dsa', 'wasa']
    expect(wrapper.find('#tag-list').classes()).toContain('col-8')
    wrapper.vm.clearSelection()
    expect(wrapper.vm.selectedTags).toEqual([])
    expect(tagListSpy).toHaveBeenCalled()
  })
})
