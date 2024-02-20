import rubpy

class ReportObject:
    async def report_object(
            self: "rubpy.Client",
            object_guid: str,
            report_type: "rubpy.enums.ReportType",
            description: str = None,
            report_type_object: str = 'Object',
    ):
        input = dict(
            object_guid=object_guid,
            report_description=description,
            report_type=report_type,
            report_type_object=report_type_object,
        )
        return await self.builder(
            name='reportObject',
            input=input,
        )