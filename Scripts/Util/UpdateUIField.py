if interactive:
    wcs = service.webclientsession()
    if wcs:
        locField = wcs.findControl('1674589367574')
        if locField:
            dataBean = locField.getDataBean()
            if dataBean:
                dataBean.fireDataChangedEvent()
                dataBean.fireStructureChangedEvent()
                dataBean.fireChildChangedEvent()
