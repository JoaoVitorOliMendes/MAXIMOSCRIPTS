from psdi.common.context import UIContext

if interactive:
    context = UIContext.getCurrentContext()
    if context is not None:
        wcs = context.getWebClientSession()
        if wcs is not None:
            databean = wcs.getDataBean('JM_WKENTRY_TABLE')
            if databean is not None:
                databean.refreshTable()
