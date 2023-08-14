DROP TABLE [dbo].[L56_DOD_SX]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_SX]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[L56_DOD_SX](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[GI03] [varchar](3) NOT NULL,
	[CB01] [varchar](12) NOT NULL,
	[XB00] [varchar](6) NOT NULL,
	[CB00] [varchar](12) NOT NULL,
	[SX01] [varchar](8) NULL,
	[SX02] [varchar](8) NULL,
	[SXD2] [varchar](1) NULL,
	[SXD3] [decimal](4, 2) NULL,
	[SX03] [decimal](4, 2) NULL,
	[SX04] [varchar](3) NULL,
	[SX05] [decimal](5, 1) NULL,
	[SXD1] [varchar](1) NULL,
	[SXD4] [decimal](7, 1) NULL,
 CONSTRAINT [PK_DOD_SX_GI03_CCCCO_Assigned_CB00_XB00] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CCCCO_Assigned] ASC,
	[CB00] ASC,
	[XB00] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
