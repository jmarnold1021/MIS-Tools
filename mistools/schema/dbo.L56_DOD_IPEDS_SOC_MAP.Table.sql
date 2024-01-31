DROP TABLE [dbo].[L56_DOD_IPEDS_SOC_MAP]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_IPEDS_SOC_MAP]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[L56_DOD_IPEDS_SOC_MAP](
	[IPEDS_Categories] [varchar](200) NULL,
	[Occupation] [varchar](2) NULL,
	[EB07] [varchar](2) NULL,
	[EJ03] [varchar](6) NULL,
	[TOP_CSS_STATUS] [varchar](2) NULL,
	[2010SOC] [varchar](20) NULL
) ON [PRIMARY]
END
GO
